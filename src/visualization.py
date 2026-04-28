import numpy as np
import matplotlib.pyplot as plt
from src.image_generator import apply_s_curve_contrast_numpy
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def visualize_bde_results(input_img: np.ndarray, output_img: np.ndarray, target_img: np.ndarray, strength: float = 20.0, titles: list[str] | None = None):
    """
    Standard visualization helper for Bit-Depth Expansion (BDE) results.
    - Row 1: INPUT, OUTPUT, TARGET (S-Curved)
    - Row 2: DIFFERENCE MAPS & GRADIENT RAMP
    """
    # Calculate Metrics
    out_hwc = np.transpose(output_img, (1, 2, 0))
    tgt_hwc = np.transpose(target_img, (1, 2, 0))
    psnr_val = psnr(tgt_hwc, out_hwc, data_range=1.0)
    ssim_val = ssim(tgt_hwc, out_hwc, data_range=1.0, channel_axis=-1)
    
    # Apply S-Curve contrast for visualization
    input_vis = apply_s_curve_contrast_numpy(input_img, strength=strength)
    output_vis = apply_s_curve_contrast_numpy(output_img, strength=strength)
    target_vis = apply_s_curve_contrast_numpy(target_img, strength=strength)
    
    # Difference map (Absolute Difference) - Model vs GT (error)
    # Using S-Curve enhanced versions to reveal quantized steps/errors
    diff_map = np.abs(output_vis - target_vis)
    diff_luma = np.mean(diff_map, axis=0) # [H, W]
    
    # Difference: Model vs Input
    diff_input = np.abs(output_vis - input_vis)
    diff_input_luma = np.mean(diff_input, axis=0)
    
    # Calculate required figure size
    dpi = 100
    h, w = input_img.shape[1], input_img.shape[2]
    
    # Create 3x2 grid (3 columns, 2 rows)
    fig = plt.figure(figsize=(18, 12), dpi=dpi)
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.2)
    
    # Row 1: S-Curved Images
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(np.transpose(input_vis, (1, 2, 0)), interpolation='nearest')
    ax0.set_title(f"8-bit Input (S-Curved {strength}x)", fontsize=12, fontweight="bold")
    ax0.axis('off')
    
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(np.transpose(output_vis, (1, 2, 0)), interpolation='nearest')
    ax1.set_title(f"Model Output (S-Curved {strength}x)", fontsize=12, fontweight="bold")
    ax1.axis('off')
    
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.imshow(np.transpose(target_vis, (1, 2, 0)), interpolation='nearest')
    ax2.set_title(f"Reference (S-Curved {strength}x)", fontsize=12, fontweight="bold")
    ax2.axis('off')
    
    # Row 2: Analysis
    # Difference: Output vs Input
    ax3 = fig.add_subplot(gs[1, 0])
    im3 = ax3.imshow(diff_input_luma, cmap='hot', interpolation='nearest')
    ax3.set_title(f"Output - Input (S-Curved)\nMean: {diff_input_luma.mean():.6f}", fontsize=11, fontweight="bold")
    ax3.axis('off')
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
    
    # Difference: Output vs Reference (Error)
    ax4 = fig.add_subplot(gs[1, 1])
    im4 = ax4.imshow(diff_luma, cmap='hot', interpolation='nearest')
    ax4.set_title(f"Output - Reference (S-Curved)\nMean: {diff_luma.mean():.6f}", fontsize=11, fontweight="bold")
    ax4.axis('off')
    plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)
    
    # Gradient Ramp Comparison
    ax5 = fig.add_subplot(gs[1, 2])
    
    # Analyze the gradient orientation to pick the best segment
    # In LuminaFlux, gradients are stacked vertically (R, G, B blocks).
    # The gradient RAMPS themselves are horizontal (color to white).
    
    # We filter out the white separator lines by only including rows that are "colorful"
    # Row-wise standard deviation helps identify the gradient rows vs the flat white/black rows
    row_vars = np.std(input_img[1, :, :], axis=1)
    
    # Find indices where there is an actual horizontal gradient (std > threshold)
    valid_row_indices = np.where(row_vars > 0.01)[0]
    
    if len(valid_row_indices) > 0:
        # Use mean across all valid gradient rows to get a clean profile and more data points
        ldr_slice = np.mean(input_img[1, valid_row_indices, :], axis=0)
        model_slice = np.mean(output_img[1, valid_row_indices, :], axis=0)
        gt_slice = np.mean(target_img[1, valid_row_indices, :], axis=0)
    else:
        # Fallback to simple slice if detection fails
        slice_y = h // 2
        ldr_slice = input_img[1, slice_y, :]
        model_slice = output_img[1, slice_y, :]
        gt_slice = target_img[1, slice_y, :]

    axis_label = "Pixel Index (Horizontal)"
    
    # Calculate unique values to determine the number of quantization buckets in the input
    # We round to handle potential floating point noise after averaging
    num_buckets = len(np.unique(np.round(ldr_slice * 255.0) / 255.0))
    
    # Zoom into the middle 10% of the X range
    x_len = len(ldr_slice)
    center = x_len // 2
    zoom_range = int(x_len * 0.025) # 2.5% on each side of center = 5% total
    x_start = max(0, center - zoom_range)
    x_end = min(x_len, center + zoom_range)
    
    indices = np.arange(x_len)
    ax5.plot(indices[x_start:x_end], ldr_slice[x_start:x_end], 'r--', label=f'8-bit Input ({num_buckets} levels)', alpha=0.8, linewidth=1)
    ax5.plot(indices[x_start:x_end], gt_slice[x_start:x_end], 'g-', label='32-bit Reference', alpha=0.6, linewidth=1.5)
    ax5.plot(indices[x_start:x_end], model_slice[x_start:x_end], 'b-', label='Model Output', alpha=0.9, linewidth=1)
    
    ax5.set_title(f"Gradient Ramp (Zoomed Middle 5%)\nInput Levels: {num_buckets}", fontsize=11, fontweight="bold")
    ax5.set_xlabel(f"{axis_label} [Center Zoom]")
    ax5.set_ylabel("Pixel Value (Green)")
    ax5.legend(fontsize=9, loc='upper left')
    ax5.grid(True, alpha=0.3, linestyle='--')
    
    # Focus Y-axis on the active range of the zoomed data
    try:
        zoom_gt = gt_slice[x_start:x_end]
        padding = (zoom_gt.max() - zoom_gt.min()) * 0.1
        if padding > 0:
            ax5.set_ylim(zoom_gt.min() - padding, zoom_gt.max() + padding)
    except:
        pass

    plt.show()
