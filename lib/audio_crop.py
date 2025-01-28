import os
import librosa
import pandas as pd
import soundfile as sf  

def crop_audio(dir, output_dir):
    """
    cropping audio files based on start and end timestamps from corresponding CSV files

    Args:
      dir: Directory containing both audio files and CSV files.
      output_dir: Directory to save cropped audio files.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(dir):
        if filename.endswith(('.wav', '.mp3')):
            audio_path = os.path.join(dir, filename)
            csv_filename = filename.replace('.wav', '.csv').replace('.mp3', '.csv')
            csv_path = os.path.join(dir, csv_filename)

            try:
                y, sr = librosa.load(audio_path)
                df = pd.read_csv(csv_path, header=None)

                start_time = df.iloc[0, 0]
                end_time = df.iloc[0, 1]

                
                start = int(start_time * sr) # converts timestamps to samples with sampling rates
                end = int(end_time * sr)

                cropped_audio = y[start:end]

                output_path = os.path.join(output_dir, filename)
                sf.write(output_path, cropped_audio, sr) 
                print(f"Cropped audio saved to: {output_path}")

            except FileNotFoundError:
                print(f"CSV file not found for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

directory = '../data/audio_dataset/train/'
output_directory = '../data/audio_dataset/train_cropped_data/'

crop_audio(directory, output_directory)