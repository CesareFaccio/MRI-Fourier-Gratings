# MRI-fourier-gratings

This program simulates how an MRI machine constructs images using sinusoidal gratings.

The program achieves this by generating gratings, similar to how an MRI does, and comparing them to the input image. This process allows the program to build a k-space, which can then be passed through an inverse Fourier transform to reconstruct the image.

There is also an option to display each step of the process, showing the current grating being compared and the image reconstruction that includes all the terms up to that point.
