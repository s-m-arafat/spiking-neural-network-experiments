import splitfolders

splitfolders.ratio(
    "../data_8k/mfcc_plots", output="../data_8k/mfcc_plots_org", seed=3, ratio=(0.7, 0.2, 0.1)
)
