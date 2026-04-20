# LuminaFlux: Bit-Depth Expansion Project

## Overview
LuminaFlux is a signal processing project focused on Bit-Depth Expansion (BDE), also known as dequantization. The goal is to upsample low-bit-depth imagery (specifically 8-bit) to high-fidelity 32-bit representations using pure signal and image processing techniques.

## Objectives
- **Bit-Depth Expansion**: Convert 8-bit images to 32-bit (float) depth while restoring original signal details that were lost during quantization.
- **Signal Processing Approach**: Utilize classical image processing algorithms, filters, and interpolation techniques instead of deep learning models.
- **Quality Metrics**: Evaluate results using Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).

## Scope
- Input: 8-bit integer-based images (standard web/consumer format).
- Output: 32-bit floating-point images.
- Focus: Restoration of contours, reduction of banding artifacts, and noise management.
