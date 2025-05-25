import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import librosa

def generate_stft_plot(audio_path, output_path):
    # Load audio file
    audio, sr = librosa.load(audio_path, sr=None)
    
    # Convert audio to PyTorch tensor
    audio_tensor = torch.from_numpy(audio).float()
    
    # Compute STFT using PyTorch
    n_fft = 2048
    hop_length = n_fft // 2
    window = torch.hann_window(n_fft)
    
    # Compute STFT
    stft = torch.stft(
        audio_tensor,
        n_fft,
        hop_length,
        n_fft,
        window,
        center=True,
        pad_mode='reflect',
        normalized=True,
        onesided=True,
        return_complex=True
    )
    
    # Get the magnitude of the complex STFT values
    stft_magnitude = torch.abs(stft)
    stft_magnitude = stft_magnitude.squeeze().numpy()
    
    # Create plot
    plt.figure(figsize=(10, 5))
    plt.gca().axis('off')  # Remove all axes
    
    # Plot the STFT
    plt.imshow(librosa.amplitude_to_db(stft_magnitude, ref=np.max),
                cmap='gray',
                aspect='auto',
                origin='lower')
    
    # Save plot
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def main():
    input_dir = "/media/arafat/New Volume/UrbanSound8K_Organized"
    output_dir = '../data_8k/stft_plots'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Walk through input directory
    for root, dirs, files in os.walk(input_dir):
        print(f"Processing {root}")
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