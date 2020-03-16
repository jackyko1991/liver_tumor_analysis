# Liver Tumor Embolization Analysis

This project focus on blood supply of liver tumor with pre- and post- embolization treatment. CBCT are scanned in plain, hepatic arterial (HA) and hepatic portal vein (PV) phase. The plain image provides larger field of view coverage while HA and PV phases are captured as time dynamic sequences.

## Analysis steps
1. Dicom extraction and NIFTI conversion
2. Tumor region localization (by cropping plain image)
3. Perform segmentation on the localized region (all images)
3. Image registration and resampling (fixed: plain, moving: HA/PV series, bspline fitting with bad registration discarded)
5. Image subtraction (contrast - plain) / temporal mIP