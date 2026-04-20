import numpy as np
import matplotlib.pyplot as plt
from src.image_generator import apply_s_curve_contrast_numpy
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def visualize_bde_results(input_img: np.ndarray, output_img: np.ndarray, target_img: np.ndarray, strength: float = 20.0, titles: list[str] | None = None):
    """
    Standard visualization helper for Bit-Depth Expansion (BDE) results.
    - Row 1: INPUT, OUTPUT, TARGET (1:1 pixel mapping)
    - Row 2: DIFFERENCE (Range Expanded), METRICS TABLE
    """
    display_max = 0.01
    
    if titles is None:
        titles = [
            "INPUT (8-bit)", 
            "OUTPUT (BDE)", 
            "TARGET (32-bit Ref)", 
            f"DIFF (Range [0, {display_max}])"
        ]
        
    # Calculate Metrics
    out_hwc = np.transpose(output_img, (1, 2, 0))
    tgt_hwc = np.transpose(target_img, (1, 2, 0))
    psnr_val = psnr(tgt_hwc, out_hwc, data_range=1.0)
    ssim_val = ssim(tgt_hwc, out_hwc, data_range=1.0, channel_axis=-1)
    
    # Apply S-Curve contrast for visualization
    input_vis = apply_s_curve_contrast_numpy(input_img, strength=strength)
    output_vis = apply_s_curve_contrast_numpy(output_img, strength=strength)
    target_vis = apply_s_curve_contrast_numpy(target_img, strength=strength)
    
    # Difference map (Absolute Difference)
    # Expand the 0-0.01 range into 0-1 for visibility
    diff = np.abs(target_img - output_img)
    diff_vis = np.clip(diff / display_max, 0, 1)
    
    # Calculate required figure size in inches for 1:1 pixel mapping (Row 1)
    dpi = 100
    h, w = input_img.shape[1], input_img.shape[2]
    
    # Grid layout: 2 rows, 3 columns
    fig = plt.figure(figsize=((w * 3) / dpi, (h * 2) / dpi), dpi=dpi)
    gs = fig.add_gridspec(2, 3)
    
    # Row 1
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(np.transpose(input_vis, (1, 2, 0)))
    ax0.set_title(titles[0])
    ax0.axis('off')
    
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(np.transpose(output_vis, (1, 2, 0)))
    ax1.set_title(titles[1])
    ax1.axis('off')
    
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.imshow(np.transpose(target_vis, (1, 2, 0)))
    ax2.set_title(titles[2])
    ax2.axis('off')
    
    # Row 2
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(np.transpose(diff_vis, (1, 2, 0)))
    ax3.set_title(titles[3] if len(titles) > 3 else f"DIFF (Range [0, {display_max}])")
    ax3.axis('off')
    
    # Metrics Table
    ax4 = fig.add_subplot(gs[1, 1:])
    ax4.axis('tight')
    ax4.axis('off')
    
    table_data = [
        ['Metric', 'Value'],
        ['PSNR', f"{psnr_val:.2f} dB"],
        ['SSIM', f"{ssim_val:.4f}"],
        ['Contrast', f"{strength}x"],
        ['Diff Range', f"0 to {display_max}"]
    ]
    
    table = ax4.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5) # Scale for readability within the grid
    ax4.set_title("Performance Metrics", fontsize=14)
        
    plt.tight_layout()
    plt.show()
