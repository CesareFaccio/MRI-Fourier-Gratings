import numpy as np
import matplotlib.pyplot as plt

class methods:

    def get_image(file_path):
        """
        creates numpy array with odd sizes from image
        """
        image = plt.imread(file_path)
        image = image[:, :, :3].mean(axis=2)
        array_size = min(image.shape) - 1 + min(image.shape) % 2
        image = image[:array_size, :array_size]

        return image

    def create_grating(size, kx, ky):
        """
        Creates a sinusoidal grating for the given spatial frequencies (kx, ky).
        """
        x = np.arange(size)
        y = np.arange(size)
        X, Y = np.meshgrid(x, y)

        grating = np.exp(-2j * np.pi * (kx * X / size + ky * Y / size))

        return grating

    def reconstruct_image(k_space):
        """
        Applies Inverse Fourier Transform to reconstruct the image.
        """
        image_reconstructed = np.fft.ifft2(np.fft.ifftshift(k_space))
        return np.abs(image_reconstructed)

class mriScan:

    def compute_k_space_using_gratings(image, max_frequency):
        """
        Compute k-space by dot product of the image with sinusoidal gratings for each kx, ky.
        - doesn't display steps. Faster method.
        """
        size = image.shape[0]
        k_space = np.zeros((size, size), dtype=complex)
        k_space_points = []

        for kx in range(-max_frequency, max_frequency + 1):
            for ky in range(-max_frequency, max_frequency + 1):
                distance = np.sqrt(kx ** 2 + ky ** 2)
                k_space_points.append((kx, ky, distance))

        k_space_points.sort(key=lambda point: point[2])

        for kx, ky, _ in k_space_points:
            grating = methods.create_grating(size, kx, ky)
            k_space[kx, ky] = np.sum(image * grating)

        return k_space

    def compute_k_space_showing_steps(image, max_frequency):
        """
        Compute k-space by dot product of the image with sinusoidal gratings for each kx, ky.
        - display each step, much slower but good for understanding.
        """
        size = image.shape[0]
        k_space = np.zeros((size, size), dtype=complex)
        k_space_points = []

        for kx in range(-max_frequency, max_frequency + 1):
            for ky in range(-max_frequency, max_frequency + 1):
                distance = np.sqrt(kx ** 2 + ky ** 2)
                k_space_points.append((kx, ky, distance))

        k_space_points.sort(key=lambda point: point[2])

        for kx, ky, _ in k_space_points:
            grating = methods.create_grating(size, kx, ky)
            grating_real = np.real(grating)

            k_space[kx, ky] = np.sum(image * grating)

            final = methods.reconstruct_image(k_space.copy())

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))  # Create two subplots side by side

            ax1.imshow(grating_real.T, cmap="gray", extent=[0, size, 0, size])
            ax1.set_title(f"Grating with kx={kx}, ky={ky}")
            ax1.axis('off')
            ax1.grid(False)

            ax2.imshow(final, cmap="gray", extent=[0, size, 0, size])
            ax2.set_title(f"image up to current term")
            ax2.axis('off')
            ax2.grid(False)

            plt.tight_layout()
            plt.show()

        return k_space

class visualise:

    def visualize_results(image, k_space, reconstructed_image):
        """
        Visualizes the phantom (spatial domain), k-space, and reconstructed image.
        """
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 3, 1)
        plt.title("Original Image")
        plt.imshow(image, cmap="gray")
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title("K-space")
        plt.imshow(np.log(np.abs(k_space) + 1), cmap="gray")
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.title("Reconstructed Image")
        plt.imshow(reconstructed_image, cmap="gray")
        plt.axis('off')

        plt.tight_layout()
        plt.show()