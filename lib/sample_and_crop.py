import os
import random
import csv
import shutil
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

# paths
source_dir = "/media/arafat/Arafat/UrbanSound/data"
destination_audio_dir = "/media/arafat/Windows/dataset"

# Ensure the destination directories exist
os.makedirs(destination_audio_dir, exist_ok=True)

# Iterate through each class directory in the source directory
for class_name in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_name)

    # Ensure it's a directory
    if not os.path.isdir(class_path):
        continue

    # Create the corresponding directory in the destination audio directory
    class_dest_audio_path = os.path.join(destination_audio_dir, class_name)
    os.makedirs(class_dest_audio_path, exist_ok=True)

    # List all audio files in the class directory
    audio_files = [
        f
        for f in os.listdir(class_path)
        if f.endswith((".wav", ".mp3", ".flac", ".aac"))
    ]

    # Check if there are any audio files in the class directory
    if not audio_files:
        print(f"No audio files found in {class_path}. Skipping this class.")
        continue

    # Process each selected audio file
    for audio_file in audio_files:
        audio_file_path = os.path.join(class_path, audio_file)

        # Find and process the corresponding CSV file
        base_name = os.path.splitext(audio_file)[0]
        csv_file = f"{base_name}.csv"
        json_file = f"{base_name}.json"

        csv_file_path = os.path.join(class_path, csv_file)
        json_file_path = os.path.join(class_path, json_file)

        if not os.path.exists(csv_file_path):
            print(f"No CSV file found for {audio_file}")
            continue

        # Read the CSV file
        try:
            with open(csv_file_path, mode="r") as file:
                csv_reader = list(csv.reader(file))
        except Exception as e:
            print(f"Error reading CSV file {csv_file_path}: {e}")
            continue

        # Load the audio file using pydub with error handling
        try:
            audio = AudioSegment.from_file(audio_file_path)
        except CouldntDecodeError as e:
            print(f"Could not decode audio file {audio_file_path}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error loading {audio_file_path}: {e}")
            continue

        # Split the audio file based on the timestamps in the CSV
        for i, row in enumerate(csv_reader, start=1):
            try:

                start_time, end_time = map(float, row[:2])
                start_time_ms = int(start_time * 1000)
                end_time_ms = int(end_time * 1000)

                # Validate time ranges
                if start_time_ms < 0 or end_time_ms < 0 or start_time_ms >= end_time_ms:
                    raise ValueError("Invalid timestamp values")

                # Split the audio segment
                split_audio = audio[start_time_ms:end_time_ms]

                # Create a new filename for the split audio file
                split_audio_filename = f"{base_name}_{i}.wav"
                split_audio_filepath = os.path.join(
                    class_dest_audio_path, split_audio_filename
                )

                # Export the split audio file
                split_audio.export(split_audio_filepath, format="wav")
            except (ValueError, IndexError) as e:
                print(f"Skipping invalid row {i} in {audio_file}: {row} - Error: {e}")
            except Exception as e:
                print(f"Error processing row {i} in {audio_file}: {e}")

        # Copy the CSV file to the class destination audio directory
        try:
            shutil.copy2(csv_file_path, class_dest_audio_path)
        except Exception as e:
            print(f"Error copying CSV file {csv_file_path}: {e}")

        # Copy the JSON file to the class destination audio directory
        if os.path.exists(json_file_path):
            try:
                shutil.copy2(json_file_path, class_dest_audio_path)
            except Exception as e:
                print(f"Error copying JSON file {json_file_path}: {e}")

print("Processing completed. Some files may have been skipped due to errors.")