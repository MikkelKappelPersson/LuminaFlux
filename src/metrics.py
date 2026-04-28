from __future__ import annotations
import numpy as np
import torch
from skimage.metrics import peak_signal_noise_ratio as psnr_func
from skimage.metrics import structural_similarity as ssim_func
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity

def compute_psnr(pred: np.ndarray, target: np.ndarray) -> float:
    """Compute PSNR between two [C, H, W] float32 images in range [0, 1]."""
    return float(psnr_func(target, pred, data_range=1.0))

def compute_ssim(pred: np.ndarray, target: np.ndarray) -> float:
    """Compute SSIM between two [C, H, W] float32 images."""
    # skimage expects [H, W, C]
    pred_hwc = np.transpose(pred, (1, 2, 0))
    target_hwc = np.transpose(target, (1, 2, 0))
    return float(ssim_func(target_hwc, pred_hwc, channel_axis=-1, data_range=1.0))

def compute_lpips(pred: np.ndarray, target: np.ndarray, net_type: str = 'vgg') -> float:
    """
    Compute LPIPS distance between two [C, H, W] float32 images.
    Lower is better (0.0 means identical).
    """
    # Initialize metric (ensuring it's on CPU for this simple check, or moves automatically)
    lpips_metric = LearnedPerceptualImagePatchSimilarity(net_type=net_type, normalize=True)
    
    # Convert [C, H, W] to [1, C, H, W] tensors
    # Ensure they are float32
    pred_t = torch.from_numpy(pred).unsqueeze(0).float()
    target_t = torch.from_numpy(target).unsqueeze(0).float()
    
    with torch.no_grad():
        score = lpips_metric(pred_t, target_t)
    return float(score.item())
