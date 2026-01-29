import os
from PIL import Image, ImageChops, ImageEnhance

def convert_to_ela_image(path, quality):
    """
    Generates an ELA image by saving the original at a specific quality
    and calculating the difference (compression noise).
    """
    original = Image.open(path).convert('RGB')
    
    # Save the image to a temporary buffer at specific quality (90%)
    resaved_name = 'temp_resaved.jpg'
    original.save(resaved_name, 'JPEG', quality=quality)
    resaved = Image.open(resaved_name)

    # Calculate the difference between the original and the resaved image
    ela_image = ImageChops.difference(original, resaved)

    # Calculate the scale factor to make the noise visible
    # We find the maximum difference and scale it up to 255 (white)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    
    if max_diff == 0:
        max_diff = 1 # Avoid division by zero
        
    scale = 255.0 / max_diff

    # Amplify the difference so human eyes can see it
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    # Cleanup temp file
    if os.path.exists(resaved_name):
        os.remove(resaved_name)

    return ela_image