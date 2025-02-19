import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def generate_stft_plot(audio_path, output_path):
    # Load audio file
    audio, sr = librosa.load(audio_path, sr=None)
    
    # Compute STFT
    n_fft = 512
    hop_length = 256
    win_length = 512
    stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window='hann')
    stft = librosa.amplitude_to_db(abs(stft), ref=np.max)
    
    # Create plot
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(stft, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', cmap='viridis', vmin=-80, vmax=0)
    
    # Remove all labels, ticks, and scaling
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().set_xlabel('')
    plt.gca().set_ylabel('')
    plt.gca().set_title('')
    plt.gca().axis('off')  # Remove all axes
    
    # Save plot
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def main():
    input_dir = "../data/urban_sound"
    output_dir = '../data/stft_plots'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Walk through input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.wav'):
                input_path = os.path.join(root, file)
                # Create corresponding output path
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_path = os.path.join(output_subdir, os.path.splitext(file)[0] + '.png')
                
                # Process audio file
                generate_stft_plot(input_path, output_path)

if __name__ == "__main__":
    main()