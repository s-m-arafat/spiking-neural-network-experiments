import splitfolders

splitfolders.ratio(
    "../data_8k/stft_plots", output="../data_8k/stft_plots_org", seed=3, ratio=(0.7, 0.2, 0.1)
)
