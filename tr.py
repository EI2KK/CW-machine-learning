import numpy as np
import os
import random

# Wczytanie pliku .npy
#label_data = np.load('json_folder_001_014/label_00001.npy', allow_pickle=True)
#data = np.load('json_folder_001_014/cw_00001.npy', allow_pickle=True)
#spectrogram_data_transposed = data.T

# Correcting the method of slicing the spectrogram data to match the provided method
def create_training_data_matching_method(cw_data_transposed, label_data, time_steps=22, overlap=11):
    # Prepare the training data structure
    training_data = {
        "file": [
            {
                "sequence": []
            }
        ]
    }

    # Initialize variables for slicing the spectrogram data
    x = 0
    z = 1  # Sequence counter

    # Iterate through the spectrogram data
    while x <= cw_data_transposed.shape[0]:
        end = x + time_steps
        # Handling the case where the last sequence is shorter than 22 steps
        if end > cw_data_transposed.shape[0]:
            spectrogram_sequence = np.zeros((time_steps, cw_data_transposed.shape[1]))
            spectrogram_sequence[:cw_data_transposed.shape[0] - x, :] = cw_data_transposed[x:end, :]
        else:
            spectrogram_sequence = cw_data_transposed[x:end, :]

        # Get the corresponding label sequence, handling the end of the label data
        label_sequence = label_data[z - 1] if z - 1 < len(label_data) else label_data[-1]

        # Append the sequence data
        training_data["file"][0]["sequence"].append({
            "data": spectrogram_sequence,
            "labels": label_sequence
        })

        x += overlap
        z += 1

    return training_data
    
    
def load_and_process_data(data_folder):
    training_data_all_files = []

    # List all .npy files in the data folder
    files = os.listdir(data_folder)
    data_files = sorted([file for file in files if file.startswith("cw_") and file.endswith(".npy")])
    label_files = sorted([file for file in files if file.startswith("label_") and file.endswith(".npy")])

    for data_file, label_file in zip(data_files, label_files):
        # Load data and labels with allow_pickle set to True
        data = np.load(os.path.join(data_folder, data_file), allow_pickle=True)
        label_data = np.load(os.path.join(data_folder, label_file), allow_pickle=True)

        spectrogram_data_transposed = data.T
        training_data = create_training_data_matching_method(spectrogram_data_transposed, label_data)

        training_data_all_files.append(training_data)

    return training_data_all_files

# Użycie funkcji
data_folder = 'json_folder_001_014'
all_training_data = load_and_process_data(data_folder)

train_percent = 0.8

# Mieszanie danych
random.shuffle(all_training_data)

# Określenie liczby plików do treningu
num_train_files = int(len(all_training_data) * train_percent)

# Podział na dane treningowe i walidacyjne
train_data = all_training_data[:num_train_files]
validation_data = all_training_data[num_train_files:]


# Check the first and last training data sequences
first_sequence_matched = all_training_data[0]["file"][0]["sequence"][0]
last_sequence_matched = all_training_data[0]["file"][0]["sequence"][-1]

#print(first_sequence_matched["data"].shape, last_sequence_matched["data"].shape, len(all_training_data[0]["file"][0]["sequence"]))

print(all_training_data[0]["file"][0]["sequence"][30]) 

