"""
Phishing Detection using Vision Transformer + DOM Fusion
Fine-tuned ViT on website screenshots with late fusion
"""

import torch
import torch.nn as nn
import pytorch_lightning as pl
from transformers import ViTForImageClassification, ViTFeatureExtractor
from transformers import AutoModel, AutoTokenizer
from typing import Dict, Tuple
import xgboost as xgb


class PhishingViTModule(pl.LightningModule):
    """
    Vision Transformer for phishing detection from website screenshots
    """
    
    def __init__(
        self,
        vit_model: str = "google/vit-base-patch16-224",
        num_classes: int = 2,
        learning_rate: float = 1e-4,
        freeze_backbone: bool = False
    ):
        super().__init__()
        self.save_hyperparameters()
        
        # Load pretrained ViT
        self.vit = ViTForImageClassification.from_pretrained(
            vit_model,
            num_labels=num_classes,
            ignore_mismatched_sizes=True
        )
        
        # Freeze backbone if needed
        if freeze_backbone:
            for param in self.vit.vit.parameters():
                param.requires_grad = False
        
        self.criterion = nn.CrossEntropyLoss()
        self.learning_rate = learning_rate
        
    def forward(self, pixel_values):
        outputs = self.vit(pixel_values=pixel_values)
        return outputs.logits
    
    def training_step(self, batch, batch_idx):
        images, labels = batch
        logits = self(images)
        loss = self.criterion(logits, labels)
        
        # Calculate accuracy
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        images, labels = batch
        logits = self(images)
        loss = self.criterion(logits, labels)
        
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        
        # Calculate probabilities for F1 score
        probs = torch.softmax(logits, dim=1)
        
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)
        
        return {'loss': loss, 'preds': preds, 'labels': labels, 'probs': probs}
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.learning_rate,
            weight_decay=0.01
        )
        
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=self.trainer.max_epochs,
            eta_min=1e-6
        )
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': scheduler
        }


class DOMEncoder(nn.Module):
    """
    Encode DOM features using BERT + TF-IDF
    """
    
    def __init__(
        self,
        bert_model: str = "bert-base-uncased",
        num_classes: int = 2,
        tfidf_dim: int = 100
    ):
        super().__init__()
        
        # BERT for text encoding
        self.bert = AutoModel.from_pretrained(bert_model)
        self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Linear(768 + tfidf_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
        
    def forward(self, text_tokens, tfidf_features):
        # BERT encoding
        bert_output = self.bert(**text_tokens)
        pooled_output = bert_output.pooler_output  # [batch, 768]
        
        # Concatenate with TF-IDF features
        combined = torch.cat([pooled_output, tfidf_features], dim=1)
        
        # Classification
        logits = self.classifier(combined)
        return logits


class LateFusionClassifier(pl.LightningModule):
    """
    Late fusion of ViT (visual) + DOM (text) for final phishing prediction
    Uses XGBoost meta-learner for fusion
    """
    
    def __init__(
        self,
        vit_module: PhishingViTModule,
        dom_encoder: DOMEncoder,
        num_classes: int = 2,
        learning_rate: float = 1e-4
    ):
        super().__init__()
        self.save_hyperparameters(ignore=['vit_module', 'dom_encoder'])
        
        self.vit = vit_module
        self.dom = dom_encoder
        
        # Freeze pre-trained models
        for param in self.vit.parameters():
            param.requires_grad = False
        for param in self.dom.parameters():
            param.requires_grad = False
        
        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(4, 64),  # 2 logits from ViT + 2 from DOM
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )
        
        self.criterion = nn.CrossEntropyLoss()
        self.learning_rate = learning_rate
        
    def forward(self, image, text_tokens, tfidf_features):
        # Get predictions from both branches
        with torch.no_grad():
            vit_logits = self.vit(image)
            dom_logits = self.dom(text_tokens, tfidf_features)
        
        # Concatenate logits
        combined_logits = torch.cat([vit_logits, dom_logits], dim=1)
        
        # Fusion
        final_logits = self.fusion(combined_logits)
        return final_logits
    
    def training_step(self, batch, batch_idx):
        images, text_tokens, tfidf_features, labels = batch
        logits = self(images, text_tokens, tfidf_features)
        loss = self.criterion(logits, labels)
        
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        images, text_tokens, tfidf_features, labels = batch
        logits = self(images, text_tokens, tfidf_features)
        loss = self.criterion(logits, labels)
        
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        
        # Get probabilities
        probs = torch.softmax(logits, dim=1)
        
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)
        
        return {'preds': preds, 'labels': labels, 'probs': probs}
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.learning_rate
        )
        return optimizer


if __name__ == "__main__":
    # Test model instantiation
    vit_model = PhishingViTModule()
    print(f"ViT Model parameters: {sum(p.numel() for p in vit_model.parameters()):,}")
    
    dom_model = DOMEncoder()
    print(f"DOM Model parameters: {sum(p.numel() for p in dom_model.parameters()):,}")
