import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_stft(stft_data, output_dir):
    """
    Plots the STFT data and saves the plots to a specified directory.

    Args:
        stft_data (dict): A dictionary where keys are filenames and values are the corresponding STFT matrices.
        output_dir (str): Directory to save the plots.
    """

    for filename, stft in stft_data.items():
        # Calculate time axis for both plots
        sr = 22050  # Assuming a standard sampling rate
        time_axis = np.arange(stft.shape[1]) * (stft.shape[1] / sr)  # Time axis for STFT

        # Create a figure with two rows and shared x-axis
        fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

        # Plot the STFT in the second row
        librosa.display.specshow(
            librosa.amplitude_to_db(stft, ref=np.max),
            sr=sr,
            x_axis="time",
            y_axis="hz",
            cmap="viridis",
            ax=axs[1],
        )
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Frequency (Hz)")

        # Layout so plots do not overlap
        fig.tight_layout()

        # Save the plot to the output directory
        filename_without_extension = os.path.splitext(filename)[0]
        plt.savefig(
            os.path.join(output_dir, f"{filename_without_extension}_stft.png")
        )
        plt.close()
