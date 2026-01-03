"""
Model Training Script for Job Scam Detection
Trains ML models on job posting dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE
import pickle
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScamDetectorTrainer:
    """Train and evaluate job scam detection models"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.vectorizer = None
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_data(self):
        """
        Load training data
        
        Expected CSV format:
        - text: Job posting text (or title/description columns)
        - label: 0 (legitimate) or 1 (scam) (or 'fraudulent' column)
        """
        if not self.data_path or not os.path.exists(self.data_path):
            logger.warning("No data file found. Creating sample dataset...")
            return self._create_sample_data()
        
        logger.info(f"Loading data from {self.data_path}")
        df = pd.read_csv(self.data_path)
        
        # Handle different column formats
        if 'fraudulent' in df.columns:
            # Handle fake_job_postings.csv format
            logger.info("Detected fake_job_postings.csv format")
            # Combine relevant text fields
            df['text'] = (
                df['title'].fillna('') + ' ' + 
                df['company_profile'].fillna('') + ' ' + 
                df['description'].fillna('') + ' ' + 
                df['requirements'].fillna('') + ' ' + 
                df['benefits'].fillna('')
            )
            df['label'] = df['fraudulent']
        
        # Validate columns
        if 'text' not in df.columns or 'label' not in df.columns:
            raise ValueError("Dataset must have 'text' and 'label' columns")
        
        return df
    
    def _create_sample_data(self):
        """Create sample dataset for demonstration"""
        samples = [
            # Legitimate jobs
            ("Software Engineer position at Tech Corp. Requirements: 3+ years Python experience, BS in CS. Competitive salary and benefits.", 0),
            ("Marketing Manager role. Lead digital campaigns, manage team of 5. MBA preferred. Salary $80k-$100k.", 0),
            ("Data Analyst needed. Work with SQL, Python, Tableau. Remote friendly. Contact hr@techcompany.com", 0),
            ("Customer Service Representative. Handle inquiries, solve problems. Training provided. Apply at careers.company.com", 0),
            ("Graphic Designer position. 2+ years Adobe Suite experience. Portfolio required. Salary negotiable.", 0),
            
            # Scam jobs
            ("URGENT!!! Earn $500 per day from home! No experience needed! Pay $99 registration fee to start!!!", 1),
            ("Work from home opportunity! Make $5000/week guaranteed! No interview required! WhatsApp only: 555-0123", 1),
            ("Personal Assistant needed. Process payments via gift cards. Pay $50 training fee. Immediate joining!", 1),
            ("Crypto trading job! Earn $1000 daily! Limited slots! Register now for $149. No skills needed!", 1),
            ("Data entry work! $300/day guaranteed! Processing fee $75. Contact telegram @scammer. Urgent hiring!", 1),
            ("Package forwarding job. Receive packages at home, reship them. Pay $100 admin fee. Easy money!!!", 1),
            ("Online survey job! $200 per hour!!! Pay small registration fee. Work from anywhere! Act now!", 1),
            ("Investment opportunity job! Bitcoin trading! Make $10000/month! Pay $199 startup fee!", 1),
        ]
        
        df = pd.DataFrame(samples, columns=['text', 'label'])
        logger.info(f"Created sample dataset with {len(df)} examples")
        return df
    
    def prepare_data(self, df, test_size=0.2):
        """Split and vectorize data"""
        logger.info("Preparing data...")
        
        X = df['text']
        y = df['label']
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Text vectorization
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.9
        )
        
        self.X_train_vec = self.vectorizer.fit_transform(self.X_train)
        self.X_test_vec = self.vectorizer.transform(self.X_test)
        
        logger.info(f"Train size: {len(self.X_train)}, Test size: {len(self.X_test)}")
        logger.info(f"Feature count: {self.X_train_vec.shape[1]}")
        
        # Handle class imbalance with SMOTE
        if len(np.unique(self.y_train)) > 1:
            try:
                smote = SMOTE(random_state=42)
                self.X_train_vec, self.y_train = smote.fit_resample(
                    self.X_train_vec, self.y_train
                )
                logger.info(f"Applied SMOTE. New train size: {len(self.y_train)}")
            except ValueError as e:
                logger.warning(f"SMOTE failed: {e}. Proceeding without resampling.")
    
    def train_model(self, model_type='ensemble'):
        """
        Train the model
        
        Args:
            model_type: 'logistic', 'random_forest', or 'ensemble'
        """
        logger.info(f"Training {model_type} model...")
        
        if model_type == 'logistic':
            self.model = LogisticRegression(
                C=1.0,
                max_iter=1000,
                class_weight='balanced',
                random_state=42
            )
        
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                class_weight='balanced',
                random_state=42
            )
        
        elif model_type == 'ensemble':
            # Ensemble of multiple models
            lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
            rf = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)
            
            self.model = VotingClassifier(
                estimators=[('lr', lr), ('rf', rf)],
                voting='soft'
            )
        
        # Train
        self.model.fit(self.X_train_vec, self.y_train)
        logger.info("Training complete!")
    
    def evaluate(self):
        """Evaluate model performance"""
        logger.info("Evaluating model...")
        
        # Predictions
        y_pred = self.model.predict(self.X_test_vec)
        y_pred_proba = self.model.predict_proba(self.X_test_vec)[:, 1]
        
        # Metrics
        print("\n" + "="*50)
        print("CLASSIFICATION REPORT")
        print("="*50)
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Legitimate', 'Scam']))
        
        print("\n" + "="*50)
        print("CONFUSION MATRIX")
        print("="*50)
        print(confusion_matrix(self.y_test, y_pred))
        
        # ROC AUC
        try:
            roc_auc = roc_auc_score(self.y_test, y_pred_proba)
            print(f"\nROC AUC Score: {roc_auc:.4f}")
        except:
            logger.warning("Could not calculate ROC AUC")
        
        print("="*50 + "\n")
    
    def save_model(self, output_path='models/saved_models/scam_detector.pkl'):
        """Save trained model and vectorizer"""
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save model and vectorizer together
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer
        }
        
        with open(output_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {output_path}")
    
    def test_predictions(self):
        """Test model on sample inputs"""
        test_samples = [
            "Software Engineer at Google. 5 years experience required. Competitive salary.",
            "URGENT!!! Make $500/day! Pay $99 fee! No interview! WhatsApp only!!!",
            "Data Analyst position. Remote work. $70k salary. Apply at careers.company.com",
            "Work from home! $5000/week guaranteed! Limited slots! Processing fee required!",
        ]
        
        print("\n" + "="*50)
        print("SAMPLE PREDICTIONS")
        print("="*50)
        
        for text in test_samples:
            vec = self.vectorizer.transform([text])
            pred = self.model.predict(vec)[0]
            proba = self.model.predict_proba(vec)[0]
            
            label = "SCAM" if pred == 1 else "LEGITIMATE"
            confidence = proba[pred]
            
            print(f"\nText: {text[:70]}...")
            print(f"Prediction: {label} (confidence: {confidence:.2%})")
        
        print("="*50 + "\n")


def main():
    """Main training pipeline"""
    print("="*60)
    print("JOB SCAM DETECTION - MODEL TRAINING")
    print("="*60 + "\n")
    
    # Initialize trainer
    trainer = ScamDetectorTrainer(data_path='data/raw/fake_job_postings.csv')
    
    # Load data
    df = trainer.load_data()
    
    # Prepare data
    trainer.prepare_data(df)
    
    # Train model
    trainer.train_model(model_type='ensemble')
    
    # Evaluate
    trainer.evaluate()
    
    # Test predictions
    trainer.test_predictions()
    
    # Save model
    trainer.save_model()
    
    print("\n✅ Training complete! Model saved to models/saved_models/scam_detector.pkl")
    print("   You can now run the API server with: python backend/main.py")


if __name__ == "__main__":
    main()
