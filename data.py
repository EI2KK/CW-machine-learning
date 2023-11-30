import os
import json
import numpy as np
import random


def process_sequence_elements(sequence, num_time_steps=22):
    # Inicjalizacja struktury etykiet dla całej porcji danych
    labels_for_this_portion = np.zeros((num_time_steps, 9))  # Zakładając, że etykiety mają 9 elementów

    for i, step in enumerate(sequence['steps']):
        if i >= num_time_steps:
            break  # Zapobieganie przekroczeniu liczby kroków

        if step['events']:  # Sprawdzenie, czy są jakieś zdarzenia w tym kroku
            event = step['events'][0]  # Przyjmowanie pierwszego zdarzenia dla uproszczenia
            element_one_hot = [int(char) for char in event['element']]
            labels_for_this_portion[i, :7] = element_one_hot
            labels_for_this_portion[i, 7] = event['frequency']
            labels_for_this_portion[i, 8] = event['speed_wpm']

    return labels_for_this_portion



def load_and_process_labels(json_file_path, time_step_length_ms, num_time_steps=22):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    processed_labels = [process_sequence_elements(sequence, num_time_steps) for sequence in data['sequences']]
    return processed_labels




def split_files_into_training_and_validation(npy_folder, train_ratio=0.8):
    files = [f for f in os.listdir(npy_folder) if f.endswith('.npy')]
    random.shuffle(files)  # Mieszanie plików

    # Liczba plików przeznaczonych na trening
    num_train = int(len(files) * train_ratio)

    # Podział plików
    train_files = files[:num_train]
    validation_files = files[num_train:]

    return train_files, validation_files

# Przykład użycia
npy_folder = 'json_folder_001_014'
train_files, validation_files = split_files_into_training_and_validation(npy_folder)



def load_and_process_spectrogram(file_path, num_steps=22, num_features=33, overlap_steps=11):
   
    # Wczytanie danych spektrogramu
    spectrogram = np.load(file_path)

    # Dzielenie spektrogramu na porcje z overlapem
    num_total_steps = spectrogram.shape[1]
    portions = []

    start = 0
    while start < num_total_steps:
        end = start + num_steps
        if end > num_total_steps:
            # Uzupełnianie ostatniej porcji zerami
            portion = spectrogram[:, start:num_total_steps]
            padding = np.zeros((num_features, end - num_total_steps))
            portion = np.concatenate((portion, padding), axis=1)
        else:
            portion = spectrogram[:, start:end]

        portions.append(portion)
        start += (num_steps - overlap_steps)

    return portions


def process_files(files, npy_folder, json_folder, num_time_steps=22, num_features=33, overlap_steps=11):
    """
    Przetwarza pliki NPY i wczytuje odpowiadające im etykiety.

    :param files: Lista plików do przetworzenia.
    :param npy_folder: Ścieżka do folderu z plikami NPY.
    :param json_folder: Ścieżka do folderu z plikami JSON.
    :param num_time_steps, num_features, overlap_steps: Parametry przetwarzania danych.
    :return: Lista par (porcja danych, etykiety).
    """
    data_label_pairs = []

    for file_name in files:
        npy_file_path = os.path.join(npy_folder, file_name)
        json_file_path = os.path.join(json_folder, file_name.replace('cw_', 'label_').replace('.npy', '.json'))

        if os.path.exists(npy_file_path) and os.path.exists(json_file_path):
            # Przetwarzanie danych
            data_portions = load_and_process_spectrogram(
                npy_file_path, num_time_steps, num_features, overlap_steps
            )
            
            # Wczytywanie i przetwarzanie etykiet
            labels = load_and_process_labels(json_file_path, num_time_steps)

            # Dopasowanie etykiet do danych i dodanie do listy
            for data, label in zip(data_portions, labels):
                data_label_pairs.append((data, label))

    return data_label_pairs



def process_files_old(files, npy_folder, json_folder, num_steps=22, num_features=33, overlap_steps=11):
    
    data_label_pairs = []

    for file_name in files:
        npy_file_path = os.path.join(npy_folder, file_name)
        json_file_path = os.path.join(json_folder, file_name.replace('.npy', '.json'))

        if os.path.exists(npy_file_path) and os.path.exists(json_file_path):
            # Przetwarzanie danych
            data_portions = load_and_process_spectrogram(
                npy_file_path, num_steps, num_features, overlap_steps
            )
            
            # Wczytywanie etykiet
            labels = load_labels(json_file_path)

            # Dopasowanie etykiet do danych i dodanie do listy
            for portion in data_portions:
                data_label_pairs.append((portion, labels))

    return data_label_pairs




# Użyj funkcji prepare_data, podając odpowiednie ścieżki
json_folder = "json_folder_001_014"
npy_folder = "json_folder_001_014"

train_data_label_pairs = process_files(train_files, npy_folder, json_folder)
validation_data_label_pairs = process_files(validation_files, npy_folder, json_folder)

print(f"Liczba par danych i etykiet: {len(train_data_label_pairs)}")
if train_data_label_pairs:
    print(f"Typ pierwszego elementu: {type(train_data_label_pairs[0])}")

if train_data_label_pairs:
    data, labels = train_data_label_pairs[12]
    print(f"Wymiary danych: {data.shape}")
    print(f"Wymiary etykiet: {type(labels)}")  # Zakładając, że etykiety są w jakiejś strukturze, np. listy
    
print("========================")

for data, labels in train_data_label_pairs:
    print(f"Wymiary danych: {data.shape}")  # Zwróci (33, liczba_kroków)
    total_elements = data.shape[0] * data.shape[1]  # Liczba cech * liczba kroków
    print(f"Całkowita liczba elementów w porcji danych: {total_elements}")
    
# Dodanie informacji o etykietach
    print(f"Typ etykiet: {type(labels)}")
    
    # Jeśli etykiety są np. listą lub macierzą numpy, możesz wyświetlić ich wymiary
    if isinstance(labels, (list, np.ndarray)):
        print(f"Wymiary etykiet: {np.array(labels).shape}")
    
    # Możesz również wypisać faktyczne etykiety, aby zobaczyć ich zawartość
    print(f"Etykiety: {labels}")
    

# Tutaj masz listy 'training_data' i 'validation_data' z porcjami danych
