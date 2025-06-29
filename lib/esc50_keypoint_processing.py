
import os
import numpy as np
import pandas as pd
import librosa
from scipy.ndimage import maximum_filter
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Parameters
n_fft = 512
hop_length = 160
beta_a = 0.15
beta_r = 0.85
dt, df = 4, 4
sr = 22050
eps = 1e-4

# Paths (edit as needed)
esc50_root = "./ESC-50"
audio_dir = os.path.join(esc50_root, "audio")
meta_csv = os.path.join(esc50_root, "meta", "esc50.csv")
output_base = "./out"

# Functions
def stft(y, sr, n_fft, hop_length, eps):
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length)) ** 2
    log_S = np.log(S + eps) - np.log(eps)
    log_S = (log_S - np.min(log_S)) / (np.max(log_S) - np.min(log_S))
    return log_S

def calc_keypoints(log_S, dt, df, beta_a, beta_r):
    local_max_time = maximum_filter(log_S, size=(1, 2 * dt + 1)) == log_S
    local_max_freq = maximum_filter(log_S, size=(2 * df + 1, 1)) == log_S
    keypoints = np.logical_or(local_max_time, local_max_freq)
    abs_mask = log_S >= beta_a
    background_mean = maximum_filter(log_S, size=(2 * df + 1, 2 * dt + 1))
    rel_mask = log_S >= beta_r * background_mean
    final_mask = keypoints & abs_mask & rel_mask
    return final_mask

def process_audio(audio_path):
    try:
        y, loaded_sr = librosa.load(audio_path, sr=sr, res_type="kaiser_fast")
        log_S = stft(y, loaded_sr, n_fft=n_fft, hop_length=hop_length, eps=eps)
        kp_mask = calc_keypoints(log_S, dt, df, beta_a, beta_r)
        freq_bins, time_bins = np.where(kp_mask)
        times = time_bins * hop_length / sr
        freqs = freq_bins * (sr / 2) / log_S.shape[0]
        return {
            'times': times,
            'freqs': freqs,
            'freq_bins': freq_bins,
            'time_bins': time_bins,
            'log_S': log_S,
            'kp_mask': kp_mask
        }
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

# Load metadata
df = pd.read_csv(meta_csv)

# Process each file
for _, row in df.iterrows():
    filename = row['filename']
    fold = row['fold']
    audio_path = os.path.join(audio_dir, filename)
    out_dir = os.path.join(output_base, f"fold_{fold}")
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    print(f"Processing {filename} in fold {fold}...")
    result = process_audio(audio_path)

    if result is not None:
        out_file = os.path.join(out_dir, f"{filename[:-4]}_keypoints.npy")
        np.save(out_file, result)
    else:
        print(f"Failed to process {filename}.")

print("ESC-50 processing complete.")
