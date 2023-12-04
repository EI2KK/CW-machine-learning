import json
import numpy as np
import os


def process_files(files, npy_folder, json_folder, num_time_steps=22, num_features=33, overlap_steps=11):
    file_data_label_pairs = []

    for file_name in files:
        npy_file_path = os.path.join(npy_folder, file_name)
        json_file_path = os.path.join(json_folder, file_name.replace('cw_', 'label_').replace('.npy', '.json'))

        if os.path.exists(npy_file_path) and os.path.exists(json_file_path):
            # Przetwarzanie danych
            data_portions = load_and_process_spectrogram(npy_file_path, num_time_steps, num_features, overlap_steps)

            # Wczytywanie i przetwarzanie etykiet
            labels = load_and_process_labels(json_file_path, num_time_steps)

            # Zbieranie danych i etykiet dla danego pliku
            data_label_pairs = list(zip(data_portions, labels))
            file_data_label_pairs.append(data_label_pairs)

    return file_data_label_pairs

def load_and_process_spectrogram(npy_file_path, num_time_steps, num_features, overlap_steps):
    # Ładowanie i transpozycja spektrogramu
    spectrogram = np.load(npy_file_path).T
    print("Transposed spectrogram shape: ", spectrogram.shape)

    # Przetwarzanie spektrogramu na porcje
    data_portions = []
    start = 0
    end = num_time_steps
    while end <= spectrogram.shape[0]:  # Uwzględnienie liczby kroków czasowych
        portion = spectrogram[start:end, :]
        if portion.shape[0] < num_time_steps:
            # Dopełnienie brakujących kroków czasowych zerami
            portion = np.pad(portion, ((0, num_time_steps - portion.shape[0]), (0, 0)), 'constant', constant_values=0)

        data_portions.append(portion)
        start += (num_time_steps - overlap_steps)
        end = start + num_time_steps

    return data_portions


def load_and_process_labels(json_file_path, num_time_steps, num_classes=7, max_events_per_step=5):
    with open(json_file_path, 'r') as file:
        labels_json = json.load(file)

    all_labels = []
    for sequence in labels_json['sequences']:
        sequence_labels = []
        for step in sequence['steps']:
            step_labels = {
                "classification": [],
                "regression": []
            }
            for event in step['events']:
                # Tworzenie wektora klasyfikacji
                classification_vector = [int(char) for char in event['element']]
                # Dodawanie wartości regresji
                regression_values = [event['frequency'], event['speed_wpm']]

                step_labels["classification"].append(classification_vector)
                step_labels["regression"].append(regression_values)

            # Dopełnienie step_labels do max_events_per_step
            while len(step_labels["classification"]) < max_events_per_step:
                step_labels["classification"].append([0] * num_classes)
                step_labels["regression"].append([0, 0])

            # Formatowanie etykiet do struktury modelu
            formatted_labels = []
            for i in range(max_events_per_step):
                formatted_labels.append((
                    step_labels["classification"][i],
                    step_labels["regression"][i]
                ))

            sequence_labels.append(formatted_labels)

        # Dopełnianie etykiet do wymaganej długości
        while len(sequence_labels) < num_time_steps:
            empty_labels = [([0] * num_classes, [0, 0]) for _ in range(max_events_per_step)]
            sequence_labels.append(empty_labels)

        all_labels.append(sequence_labels[:num_time_steps])


    return all_labels


