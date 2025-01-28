from plot import plot_stft
from audio_to_stft import audio_to_stft

stft_data = audio_to_stft("./audio_dataset")
plot_stft(stft_data, "./stft_plots/")


