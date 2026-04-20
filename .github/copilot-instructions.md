# LuminaFlux: Bit-Depth Expansion with signal processing

## Project Vision

LuminaFlux is a Singal processing project for a signal processing course. is aim to do:

-   **Bit-Depth Expansion (BDE)/Dequantization**: Upsampling low-bit-depth imagery (e.g., 8-bit, 10-bit) to higher fidelity using learned super-resolution.

## Architecture

-   Python 3.12+
##   Code Style & Language

-   **Type hints** on all function signatures; use `typing` module and `from __future__ import annotations` for forward refs.
-   **Fail Fast**: Avoid exceptions and instead fail fast or use asserts if needed.

## Domain Knowledge (Reference)

-   **Bit-depth**: Standard depths are 8, 10, 12, 16-bit; 8-bit is common in web/consumer, 10+ in cinema/HDR.
-   **Metrics**: PSNR (luminance), SSIM (structure)

**Version**: 1.0 | **Last updated**: 2026-04-20