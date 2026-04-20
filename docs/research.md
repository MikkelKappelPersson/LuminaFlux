# Research: Bit-Depth Expansion (BDE) Methods

This document explores classical signal processing methods for expanding bit-depth from 8-bit to 32-bit and mitigating quantization artifacts.

## 1. Dithering and De-quantization
Dithering is the process of adding intentionally applied noise to randomize quantization error. In the context of BDE, we are reversing this or handling images where dithering wasn't applied, leading to banding.
- **Ordered Dithering**: Uses a fixed threshold matrix (e.g., Bayer matrix).
- **Error Diffusion**:
    - **Floyd-Steinberg**: Spreads quantization error to neighboring pixels (Right: 7/16, Bottom-Left: 3/16, Bottom: 5/16, Bottom-Right: 1/16).
    - **Jarvis-Judice-Ninke**: Coarser but fewer artifacts than Floyd-Steinberg.
    - **Atkinson Dithering**: Preserves detail well but can blow out extremes.
- **Reference**: Ulichney, R. (1987). *Digital Halftoning*. MIT Press. [Link](https://mitpress.mit.edu/9780262210096/digital-halftoning/)

## 2. Interpolation Techniques
Expanding bit-depth often involves assuming a smoother transition between quantized levels.
- **Linear/Bilinear Interpolation**: Simple but results in blurry edges.
- **Bicubic Interpolation**: Smoother than bilinear, better for gradients.
- **Lanczos Resampling**: Uses a sinc filter, preserving high-frequency content better than cubic interpolation.
- **Reference**: Keys, R. (1981). "Cubic convolution interpolation for digital image processing". *IEEE Transactions on Acoustics, Speech, and Signal Processing*. [DOI: 10.1109/TASSP.1981.1163711](https://doi.org/10.1109/TASSP.1981.1163711)

## 3. Debanding & Artifact Removal
Banding (contouring) is the primary artifact of low bit-depth.
- **Adaptive Filtering**: Applying different filter strengths based on local image gradients.
- **Bilateral Filtering**: A non-linear, edge-preserving, and noise-reducing smoothing filter. It replaces the intensity of each pixel with a weighted average of intensity values from nearby pixels.
- **Reference**: Tomasi, C., & Manduchi, R. (1998). "Bilateral filtering for gray and color images". *ICCV*. [Link](https://ieeexplore.ieee.org/document/710815)

## 4. Signal Modeling
- **Total Variation (TV) Denoising**: Minimizes the total variation of the image, which helps in preserving edges while smoothing out quantization steps.
- **Reference**: Rudin, L. I., Osher, S., & Fatemi, E. (1992). "Nonlinear total variation based noise removal algorithms". *Physica D: Nonlinear Phenomena*. [DOI: 10.1016/0167-2789(92)90136-7](https://doi.org/10.1016/0167-2789(92)90136-7)

## 5. Frequency Domain Methods (Fourier Transform)
Quantization noise often manifests as high-frequency harmonics or "ghosting" in the spectrum.
- **Low-Pass Filtering (LPF)**: Since 8-bit quantization introduces sharp transitions (banding), these can be modeled as high-frequency noise. Applying a Butterworth or Gaussian LPF in the frequency domain can smooth these transitions.
- **Homomorphic Filtering**: Useful for images with non-uniform illumination where quantization artifacts are more visible.
- **Reference**: Stockham, T. G. (1972). "Image processing in the context of a visual model". *Proceedings of the IEEE*. [DOI: 10.1109/PROC.1972.8782](https://doi.org/10.1109/PROC.1972.8782)

## 6. Advanced Classical Methods
- **Guided Image Filtering**: An alternative to bilateral filtering that avoids "staircase" artifacts and gradient reversal.
- **Reference**: He, K., Sun, J., & Tang, X. (2013). "Guided Image Filtering". *IEEE TPAMI*. [DOI: 10.1109/TPAMI.2012.213](https://doi.org/10.1109/TPAMI.2012.213)
- **Intensity Potential for Adaptive De-quantization (IPAD)**: Uses adaptive low-pass filters to restore high bit-depth images.
- **Reference**: Liu, J., et al. (2018). "IPAD: Intensity potential for adaptive de-quantization". *IEEE Transactions on Image Processing*. [Link](https://ieeexplore.ieee.org/document/8283657/)

## 7. Multi-Scale & Wavelet Analysis
Frequency-based methods can be applied at different scales using Wavelet Transforms. Unlike the Fourier Transform, which only provides frequency information, the Wavelet Transform provides both time (spatial) and frequency localization, which is crucial for handling quantization artifacts that vary across the image.
- **Discrete Wavelet Transform (DWT)**: Decomposing the image into approximation (LL) and detail (LH, HL, HH) coefficients. BDE can be achieved by refining the detail coefficients using statistical models or adaptive thresholding before reconstruction.
- **Soft/Hard Thresholding**: Used to eliminate quantization noise (which often appears in the high-frequency detail coefficients) while preserving structural edges.
- **Stationary Wavelet Transform (SWT)**: Also known as the Undecimated Wavelet Transform. It omits the downsampling step of the DWT, making it shift-invariant. This is particularly useful for BDE to avoid "ringing" artifacts at edges.
- **Reference**: Mallat, S. G. (1989). "A theory for multiresolution signal decomposition: the wavelet representation". *IEEE Transactions on Pattern Analysis and Machine Intelligence*. [DOI: 10.1109/34.192463](https://doi.org/10.1109/34.192463)
- **Reference**: Donoho, D. L. (1995). "De-noising by soft-thresholding". *IEEE Transactions on Information Theory*. [DOI: 10.1109/18.382017](https://doi.org/10.1109/18.382017)

## 8. Cepstral Analysis (Homomorphic Processing)
The cepstrum is the "spectrum of a spectrum," used to investigate periodic structures and perform homomorphic deconvolution.
- **Liftering**: Applying a filter in the quefrency domain to remove specific periodic artifacts (like banding) that appear as peaks.
- **Blocking Artifact Reduction**: Effective for removing the "staircase" effects of quantization by separating the excitation signal from the image content.
- **Reference**: Bogert, B. P., et al. (1963). "The Quefrency Alanysis [sic] of Time Series for Echoes". *Proceedings of the Symposium on Time Series Analysis*.
- **Reference**: Cho, N. I. (2001). "Reduction of blocking artifacts by cepstral filtering". *Signal Processing*. [DOI: 10.1016/S0165-1684(00)00237-1](https://doi.org/10.1016/S0165-1684(00)00237-1)
