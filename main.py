from myMRI import mriScan
from myMRI import visualise
from myMRI import methods as mriMethods

def main():

    # any image can be used I choose a brain drawing for relevance
    image = mriMethods.get_image('brain.jpg')

    # shows initial few steps
    k_space = mriScan.compute_k_space_showing_steps(image, 1)

    # calculates k-space to larger degree without showing steps
    k_space = mriScan.compute_k_space_using_gratings(image, 30)

    reconstructed_image = mriMethods.reconstruct_image(k_space).T

    visualise.visualize_results(image, k_space, reconstructed_image)

if __name__ == "__main__":
    main()