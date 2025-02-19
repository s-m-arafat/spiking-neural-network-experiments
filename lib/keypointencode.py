import cv2
import numpy as np
import os

def keypoint_encode(image, threshold=0.1):
    """
    Perform key point encoding on a spectrogram image.
    Args:
        image: Input spectrogram image (H, W, C)
        threshold: Threshold for key point detection
    Returns:
        encoded_image: Key point encoded image
    """
    # Convert image to grayscale if it's not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    # Compute image gradients
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute gradient magnitude
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalize magnitude to [0, 1]
    magnitude = (magnitude - magnitude.min()) / (magnitude.max() - magnitude.min() + 1e-8)

    # Detect key points based on magnitude threshold
    key_points = magnitude > threshold

    # Create encoded image by downsampling using key points
    encoded_image = np.zeros_like(image)
    encoded_image[key_points] = image[key_points]

    return encoded_image

def process_spectrogram_directory(input_dir, output_dir, downsample_factor=4):
    """
    Process all spectrogram images in a directory and save the key point encoded images.
    Args:
        input_dir: Input directory containing spectrogram images
        output_dir: Output directory to save encoded images
        downsample_factor: Downsampling factor
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all files in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Check if file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Read image
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                if image is not None:
                    # Perform key point encoding
                    encoded_image = keypoint_encode(image)

                    # Downsample the image
                    encoded_image = cv2.resize(encoded_image, None, fx=1/downsample_factor, fy=1/downsample_factor, interpolation=cv2.INTER_LINEAR)

                    # Save encoded image
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    output_path = os.path.join(output_subdir, file)
                    cv2.imwrite(output_path, encoded_image)

                    print(f"Processed and saved: {output_path}")

# Example usage
input_directory = "../data/stft_plots_org"
output_directory = "../data/keypointencoded"

process_spectrogram_directory(input_directory, output_directory, downsample_factor=4)