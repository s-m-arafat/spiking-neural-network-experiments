import splitfolders

splitfolders.ratio(
    "../data_esc50/mfcc_plots", output="../data_esc50/mfcc_plots_org", seed=3, ratio=(0.7, 0.2, 0.1)
)
