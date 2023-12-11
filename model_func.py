import numpy as np
import os
import random
import shutil

def validate_model_on_batch(model, X, y):
    # Przeprowadź walidację i zwróć wynik
    # Możesz użyć np. model.evaluate(), model.predict() itp., w zależności od potrzeb
    evaluation = model.evaluate(X, y, verbose=0)
    return evaluation



def prepare_labels(sequence_labels, num_classes=7):
    # Struktury na dane wyjściowe dla każdej warstwy
    elements_output = [np.zeros((22, num_classes)) for _ in range(5)]  # 7 klas dla klasyfikacji
    freq_output = [np.zeros((22, 2)) for _ in range(5)]  # 2 wartości dla regresji

    for step_index, step in enumerate(sequence_labels):
        for i, event in enumerate(step['events']):
            # Przetwarzanie klasyfikacji
            element_vector = event["element"]
            elements_output[i][step_index, :] = np.array([int(x) for x in element_vector])

            # Przetwarzanie regresji
            frequency = event["frequency"]
            speed_wpm = event["speed_wpm"]
            freq_output[i][step_index, :] = [frequency, speed_wpm]

    # Połączenie danych wyjściowych w jeden zestaw
    combined_output = []
    for i in range(5):
        combined_output.extend([elements_output[i], freq_output[i]])

    return combined_output


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


def split_data(source_directory, train_ratio=0.8):
    # Utwórz ścieżki do podkatalogów
    train_directory = os.path.join(source_directory, 'training')
    validation_directory = os.path.join(source_directory, 'validation')

    # Utwórz podkatalogi, jeśli nie istnieją
    os.makedirs(train_directory, exist_ok=True)
    os.makedirs(validation_directory, exist_ok=True)

    # Wczytaj wszystkie pliki .npy
    all_files = [f for f in os.listdir(source_directory) if f.endswith('.npy')]

    # Losowe mieszanie plików
    np.random.shuffle(all_files)

    # Podział plików na treningowe i walidacyjne
    split_index = int(len(all_files) * train_ratio)
    train_files = all_files[:split_index]
    validation_files = all_files[split_index:]

    # Przenieś pliki do odpowiednich podkatalogów
    for f in train_files:
        shutil.move(os.path.join(source_directory, f), train_directory)

    for f in validation_files:
        shutil.move(os.path.join(source_directory, f), validation_directory)

