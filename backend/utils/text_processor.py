"""
Text Processing Utilities
Clean and preprocess job posting text
"""
import re
from typing import Optional


class TextProcessor:
    """Text cleaning and preprocessing"""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw job posting text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        # Keep: $ ₹ @ . , ! ? - () []
        text = re.sub(r'[^\w\s$₹@.,!?\-\(\)\[\]]', '', text)
        
        # Normalize currency symbols
        text = text.replace('₹', 'INR ')
        text = text.replace('$', 'USD ')
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_from_ocr(self, image_path: str) -> Optional[str]:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text or None
        """
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            return self.clean_text(text)
            
        except ImportError:
            raise ImportError("pytesseract not installed. Run: pip install pytesseract")
        except Exception as e:
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    def truncate_text(self, text: str, max_length: int = 5000) -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
