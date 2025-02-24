from PIL import Image
import pytesseract

def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    img = Image.open(image_path)  # Open image using PIL
    extracted_text = pytesseract.image_to_string(img)  # Perform OCR
    return extracted_text

if __name__ == "__main__":
    image_path = "/media/rskmn/D864320D6431EF3E/rskmn/theBendu/otherProjects/2-2_Project/safeLabel/work/version-0.1/work/imgs/1.png"  # Replace with your image file
    text = extract_text(image_path)

    print("\n📜 Extracted Text:\n", text)

