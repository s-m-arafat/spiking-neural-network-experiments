
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os


"""
    The function `plot_and_save_chirplet_transform` loads an audio file, performs Short-Time Fourier
    Transform (STFT), plots the STFT without axes and labels, and saves the plot as a PNG file in the
    specified output folder.
    
    :param audio_path: The `audio_path` parameter in the `plot_and_save_chirplet_transform` function is
    the file path to the audio file that you want to analyze and plot the Short-Time Fourier Transform
    (STFT) for. This function loads the audio file using librosa, performs the STFT, and
    :param output_folder: The `output_folder` parameter in the `plot_and_save_chirplet_transform`
    function is the directory path where you want to save the generated plot of the Short-Time Fourier
    Transform (STFT) without axes and labels. This parameter specifies the folder where the plot image
    will be saved as a PNG
"""
def plot_and_save_chirplet_transform(audio_path, output_folder):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Perform the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # Plot the STFT without axes and labels
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(stft_db, sr=sr, x_axis=None, y_axis=None, cmap="viridis")
    plt.axis("off")

    # Save the plot
    plot_filename = os.path.basename(audio_path).rsplit(".", 1)[0] + "_chirplet.png"
    plot_path = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_path, bbox_inches="tight", pad_inches=0)
    plt.close()


def plot_and_save_combined_waveform_and_chirplet(audio_path, output_folder):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Perform the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # Create a combined plot
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 12))

    # Plot the waveform and time axis
    librosa.display.waveshow(y, sr=sr, axis='time', ax=ax[0])
    ax[0].set(title="Waveform")

    ax[0].label_outer()

    # Plot the STFT
    img = librosa.display.specshow(
        stft_db, sr=sr, x_axis="time", y_axis="log", ax=ax[1], cmap="viridis"
    )
    ax[1].set(title="Chirplet Transform (STFT)")
    fig.colorbar(img, ax=ax[1], format="%+2.0f dB")

    # Save the combined plot
    plot_filename = os.path.basename(audio_path).rsplit(".", 1)[0] + "_combined.png"
    plot_path = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_path, bbox_inches="tight", pad_inches=0)
    plt.close()


def process_audio_files_in_folder(
    input_folder, chirplet_output_folder, combined_output_folder
):
    # Ensure output folders exist
    os.makedirs(chirplet_output_folder, exist_ok=True)
    os.makedirs(combined_output_folder, exist_ok=True)

    # Get list of all files in the folder
    audio_files = [
        f
        for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
    ]

    # Filter audio files to include only WAV, MP3, and FLAC
    audio_files = [f for f in audio_files if f.endswith((".wav", ".mp3", ".flac"))]

    for audio_file in audio_files:
        audio_path = os.path.join(input_folder, audio_file)
        plot_and_save_chirplet_transform(audio_path, chirplet_output_folder)
        plot_and_save_combined_waveform_and_chirplet(audio_path, combined_output_folder)


# Example usage
input_folder = "../data/audio_dataset/"
chirplet_output_folder = "../data/chirplet_plots/"
combined_output_folder = "../data/combined_plots/"
process_audio_files_in_folder(
    input_folder, chirplet_output_folder, combined_output_folder
)
