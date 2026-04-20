# Recommended Technical Stack: LuminaFlux

This document outlines the libraries and tools selected for performing Bit-Depth Expansion (BDE) using classical signal and image processing techniques.

## 1. Core Computation
- **[NumPy](https://numpy.org/)**: Essential for 8-bit to 32-bit (float) conversion and high-performance N-dimensional array manipulations. It will be our primary data structure for image pixels.
- **[SciPy](https://scipy.org/)**: 
    - `scipy.signal`: For FFT/Fourier analysis, Wiener filtering, and IIR/FIR filter design.
    - `scipy.interpolate`: For high-order (bicubic, spline) upsampling operations.

## 2. Image Processing & Filtering
- **[OpenCV (opencv-python)](https://opencv.org/)**: 
    - **Bilateral Filtering**: Edge-preserving smoothing to remove banding.
    - **Guided Filtering**: An efficient alternative to bilateral filters (via `opencv-contrib-python`).
    - **Optimization**: Highly optimized C++ backend for real-time performance.
- **[scikit-image (skimage)](https://scikit-image.org/)**: 
    - **Total Variation (TV) Denoising**: Using `denoise_tv_chambolle` to smooth quantization steps.
    - **Advanced Restoration**: Algorithms like Non-Local Means (NLM) adapted for dequantization.

## 3. Specialized Domain Transforms
- **[PyWavelets (pywt)](https://pywavelets.readthedocs.io/)**: 
    - **Multi-Scale Analysis**: Essential for Discrete Wavelet Transform (DWT) and Stationary Wavelet Transform (SWT) approaches to BDE.
- **[Librosa](https://librosa.org/)**: 
    - **Cepstral Analysis**: Although designed for audio, it provides robust logs-spectral and MFCC tools that can be adapted for line-by-line image analysis to remove periodic artifacts.

## 4. Metrics & Evaluation
- **[scikit-image.metrics](https://scikit-image.org/docs/stable/api/skimage.metrics.html)**: 
    - **PSNR (Peak Signal-to-Noise Ratio)**: Basic fidelity metric.
    - **SSIM (Structural Similarity Index)**: A perceptual metric for evaluating how well the expanded image preserves structures.

## 5. Development Environment
- **Python 3.12+**: Utilizing modern typing and performance optimizations.
- **Jupyter Notebooks**: For rapid prototyping, visualization of filters, and comparative analysis of different techniques.
- **Matplotlib**: For plotting frequency spectra (FFT) and side-by-side metric comparisons.
