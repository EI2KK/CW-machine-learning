import os
import json
import numpy as np
import random



def reshape_data_for_model(data):
    # Transponowanie danych, aby kroki czasowe były pierwsze
    data_transposed = data.T  # Zmiana z (33, 22) na (22, 33)
    print(data_transposed.shape)
    # Przekształcenie danych na wektor jednowymiarowy
    reshaped_data = data_transposed.reshape(-1)
    return reshaped_data


def prepare_labels_for_model(labels):
    # Zakładając, że 'labels' ma wymiary (22, 9)
    classification_labels = labels[:, :7]  # Pierwsze 7 cech dla klasyfikacji
    regression_labels = labels[:, 7:]      # Ostatnie 2 cechy dla regresji

    return [classification_labels, regression_labels]


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



print(len(validation_data_label_pairs))

prepared_labels = prepare_labels_for_model(train_data_label_pairs[0][12][1])

#print(prepared_labels[0])
#print(prepared_labels[1])
# Przykładowe użycie
# Załóżmy, że mamy przykładowe dane wejściowe 'data'
data_example = train_data_label_pairs[0][0] # np.random.rand(33, 22)  # Przykładowe dane
reshaped_data = reshape_data_for_model(data_example[0])


print(f"Przekształcone wymiary danych: {reshaped_data.shape}")


"""  
# Trenowanie modelu

best_val_accuracy = 0
patience = 10
no_improvement_epochs = 0

model = load_model('best_model.h5')

for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")
    random.shuffle(train_data_label_pairs)
    
    # Trening
    for file_data_label_pair in train_data_label_pairs:
        for data, labels in file_data_label_pair:
            model.train_on_batch(data, labels)  # Trenowanie na każdej porcji danych
            print(labels)
          
    # Walidacja
    validation_loss, validation_accuracy = 0, 0
    total_validation_batches = 0
    for file_data_label_pair in validation_data_label_pairs:
        for data, labels in file_data_label_pair:
            loss, accuracy = model.evaluate(data, labels, verbose=0)
            
            
    # Sprawdzenie, czy nastąpiła poprawa
    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        no_improvement_epochs = 0
        # Opcjonalnie: Zapisz model
        model.save('best_model.h5')
    else:
        no_improvement_epochs += 1

    # Sprawdzenie warunku early stopping
    if no_improvement_epochs >= patience:
        print(f"Early stopping po {epoch+1} epokach.")
        break
    
    


"""

"""
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
"""