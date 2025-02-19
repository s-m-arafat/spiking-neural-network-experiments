import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from brian2 import *
import glob

# Parameters
global_threshold = 0.09
block_size = 19
C = -5
sampling_factor = 10

# Input and output directories
stft_root_folder = '../data/stft_plots_org'  # e.g., 'stft_images'
spatiotemporal_root_folder = '../data/spatiotemporal_plots_2'


# Create root output folders if they don't exist
os.makedirs(spatiotemporal_root_folder, exist_ok=True)

# Define the splits
splits = ['test', 'train', 'val']

# Process each split
for split in splits:
    print(f"Processing {split} set...")
    
    # Path to current split's STFT images
    split_stft_path = os.path.join(stft_root_folder, split)
    
    # Get all class folders in the current split
    class_folders = [f for f in os.listdir(split_stft_path) if os.path.isdir(os.path.join(split_stft_path, f))]
    
    # Process each class folder
    for class_folder in class_folders:
        print(f"Processing class: {class_folder}")
        
        # Input and output paths for the current class
        class_input_path = os.path.join(split_stft_path, class_folder)
        class_spatiotemporal_path = os.path.join(spatiotemporal_root_folder, split, class_folder)
        
        # Create class-specific output folders
        os.makedirs(class_spatiotemporal_path, exist_ok=True)

        
        # Get all STFT plot files in the class folder
        stft_files = glob.glob(os.path.join(class_input_path, "*.png"))
        
        # Process each STFT plot
        for stft_file in stft_files:
            print(f"Processing file: {os.path.basename(stft_file)}")
            
            # Load the STFT plot
            image = cv2.imread(stft_file, cv2.IMREAD_GRAYSCALE)
            image_data = image.astype(float) / 255.0
            height, width = image_data.shape
            
            # Get audio path from the image path (adjust based on your naming convention)
            audio_path = stft_file.replace("_stft.png", ".wav")
            # Replace with actual code to get the audio duration
            duration = 1.0  # Replace with actual audio duration
            second = 1 * second  # Ensure 'second' is defined or remove if not needed
            
            time_duration = duration * second
            num_neurons = height
            
            # Adaptive thresholding
            adaptive_thresh = cv2.adaptiveThreshold(
                (image_data * 255).astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C
            )
            adaptive_thresh = adaptive_thresh / 255.0
            
            # Find spike times and neurons
            times = []
            neurons = []
            for ex in range(width):
                for why in range(height):
                    if image_data[why, ex] > global_threshold and adaptive_thresh[why, ex] > 0:
                        time_point = ex / width * time_duration
                        neuron_point = why
                        times.append(time_point)
                        neurons.append(neuron_point)

            times = np.array(times) * second
            neurons = np.array(neurons, dtype=int)
            
            # Create and run the Brian2 network
            G = NeuronGroup(num_neurons, 'v : 1', threshold='v>1', reset='v=0', method='exact')
            G.v = 0
            input_group = SpikeGeneratorGroup(num_neurons, indices=neurons, times=times)
            S = Synapses(input_group, G, on_pre='v_post += 1')
            S.connect(j='i')
            run(time_duration)
            
            # Sampling
            sampled_indices = np.arange(0, len(times), sampling_factor)
            
            # Create spatiotemporal plot
            fig_spatiotemp, ax_spatiotemp = plt.subplots(figsize=(7, 5))
            fig_spatiotemp.patch.set_facecolor('black')
            ax_spatiotemp.set_facecolor('black')
            
            ax_spatiotemp.scatter(times[sampled_indices] / second,
                                 num_neurons - neurons[sampled_indices] - 1, 
                                 s=10, 
                                 alpha=0.5, 
                                 edgecolor='white', 
                                 color='white')
            ax_spatiotemp.axis('off')
            ax_spatiotemp.margins(0)
            
            # Save spatiotemporal plot
            plot_filename_spatiotemp = os.path.basename(stft_file).rsplit(".", 1)[0] + "_spatiotemporal.png"
            plot_path_spatiotemp = os.path.join(class_spatiotemporal_path, plot_filename_spatiotemp)
            plt.savefig(plot_path_spatiotemp, bbox_inches="tight", pad_inches=0)
            plt.close(fig_spatiotemp)
            
            # Create combined plot
            fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(7, 10))
            
            # Plot spatiotemporal points
            ax[3].scatter(times[sampled_indices]/second, 
                         num_neurons - neurons[sampled_indices] - 1, 
                         s=10, 
                         alpha=0.5, 
                         edgecolor='black')
            ax[3].set_xlim(0, duration)
            ax[3].set_xlabel('Time (s)')
            ax[3].set_ylabel('Afferents')
            ax[3].set_title('Spatiotemporal Points from Spectrogram')
            
            plt.tight_layout()


print("Processing complete!")