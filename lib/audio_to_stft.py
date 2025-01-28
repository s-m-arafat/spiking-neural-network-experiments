'''
    Author: Shakil Mahmud Arafat, EEE AUST
    Date last updated: 28 Nov, 2024
'''

import os
import librosa
import numpy as np

def audio_to_stft(dir):
    """
    Reads audio files from a directory, performs STFT on each file,
    and returns a dictionary containing the STFT matrices.

    Args:
        dir (str): Directory containing audio files

    Returns:
        dict: A dictionary where keys are filenames and values are 
              the corresponding STFT matrices.
    """
    
    # Initialize an empty dictionary to store the STFTs final values following filenames
    stft_data = {}  

    # Loop through each file in the directory
    for filename in os.listdir(dir):
        # Check if file is an audio file
        if filename.endswith((".ogg", ".mp3")):
            
            # Read audio file using Librosa
            file_path = os.path.join(dir, filename)
            audio, sr = librosa.load(file_path)

            # Perform STFT
            stft = np.abs(librosa.stft(audio))

            # Store the STFT matrix in the dictionary with filename as key
            stft_data[filename] = stft 

    return stft_data