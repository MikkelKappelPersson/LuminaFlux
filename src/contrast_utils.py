import torch
import torch.nn.functional as F

def apply_s_curve_contrast_torch(image: torch.Tensor, strength: float = 2.0) -> torch.Tensor:
    """Apply S-curve contrast using PyTorch.
    
    Formula: S(x) = x^n / (x^n + (1-x)^n)
    where n is the strength.
    
    Args:
        image: Input tensor [..., C, H, W] in [0, 1] range
        strength: Power n (default 2.0). Higher = more contrast.
    
    Returns:
        Contrast-adjusted tensor
    """
    epsilon = 1e-7
    x = torch.clamp(image, 0, 1)
    
    # Avoid log/power issues with 0 and 1
    x_safe = torch.clamp(x, epsilon, 1 - epsilon)
    
    # Calculate s-curve
    x_power = torch.pow(x_safe, strength)
    one_minus_x_power = torch.pow(1 - x_safe, strength)
    s_curve = x_power / (x_power + one_minus_x_power)
    
    # Replace back the 0 and 1 bits
    result = torch.where(x < epsilon, torch.zeros_like(x), 
                        torch.where(x > 1 - epsilon, torch.ones_like(x), s_curve))
    
    return result
