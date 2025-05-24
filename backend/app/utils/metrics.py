import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

def calculate_metrics(original, colorized):
    """Calculate PSNR and SSIM metrics between original and colorized images."""
    # Convert to grayscale for comparison
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    colorized_gray = cv2.cvtColor(colorized, cv2.COLOR_BGR2GRAY)
    
    # Calculate metrics
    psnr_value = psnr(original_gray, colorized_gray)
    ssim_value = ssim(original_gray, colorized_gray)
    
    return {
        'psnr': float(psnr_value),
        'ssim': float(ssim_value)
    } 