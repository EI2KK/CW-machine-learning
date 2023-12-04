import os
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Attention, Input
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.models import Model
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from model_func import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ustawia poziom logowania na błędy (errors)
tf.get_logger().setLevel('ERROR')  # Dodatkowo ustawia logowanie na poziomie Pythona

# Parametry modelu - dostosuj je do swoich potrzeb
lstm_units = 256  # Liczba jednostek w warstwach LSTM
dense_units = 128  # Liczba jednostek w warstwach gęsto połączonych
num_classes = 7   # Liczba klas/etykiet do rozpoznania
dropout_rate = 0.5
learning_rate = 0.001
"""
# Wymiary danych wejściowych - należy je dostosować do Twoich danych
input_shape = (22, 33)  # 'None' dla zmiennego rozmiaru sekwencji, 'num_features' to liczba cech na krok czasowy

# Tworzenie warstwy wejściowej
input_layer = Input(shape=input_shape)

# Dodawanie warstw LSTM
lstm_layer = LSTM(lstm_units, return_sequences=True)(input_layer)
lstm_layer = LSTM(lstm_units, return_sequences=True)(lstm_layer)

# Dodawanie warstwy uwagi
attention_layer = Attention()([lstm_layer, lstm_layer])

# Dodawanie warstwy Dropout dla regularyzacji
dropout_layer = Dropout(dropout_rate)(attention_layer)

# Warstwa wspólna
common_dense = Dense(dense_units, activation='relu')(dropout_layer)

# Tworzenie warstw wyjściowych
outputs = []
for i in range(5):  # Tworzenie pięciu par wyjściowych
    # Warstwa klasyfikacji dla pary i-tej
    elements = Dense(num_classes, activation='softmax', name=f'elements_{i}')(common_dense)

    # Warstwa regresji dla pary i-tej
    freq = Dense(2, activation='linear', name=f'freq_{i}')(common_dense)

    # Dodawanie par do listy wyjść
    outputs.extend([elements, freq])

# Tworzenie modelu z wieloma wyjściami
model = Model(inputs=input_layer, outputs=outputs)
# Kompilacja modelu
model.compile(optimizer=Adam(learning_rate=learning_rate),
              loss={'classification_output': 'categorical_crossentropy',
                    'regression_output': 'mean_squared_error'},
              metrics={'classification_output': 'accuracy',
                       'regression_output': ['mae']})

# Wyświetlenie podsumowania modelu
model.summary()
"""

model_id = "01.01"
# Otwieranie pliku JSON i wczytywanie danych
with open('training.json', 'r') as file:
    data = json.load(file)

# Szukanie pierwszego rekordu bez danego model_id
for record in data:
    if model_id not in record.get("model", []):
        directory = record["directory"]
        break
directory_path = os.path.join(directory)
files = os.listdir(directory_path)

# Filtracja tylko plików .npy
npy_files = [file for file in files if file.endswith('.npy')]

file_data_label_pairs = process_files(npy_files, directory_path, directory_path, num_time_steps=22, num_features=33, overlap_steps=11)

# Analiza pierwszego pliku
first_file_pairs = file_data_label_pairs[0]

# Analiza pierwszej pary dane-etykiety
first_pair = first_file_pairs[0]
single_step_data, single_step_labels = first_pair
print("Pierwsza para:")
print("Data shape: ", single_step_data.shape)
print("Labels length: ", len(single_step_labels))
# ...

# Analiza ostatniej pary dane-etykiety
last_pair = first_file_pairs[-1]
single_step_data, single_step_labels = last_pair
print("\nOstatnia para:")
print("Data shape: ", single_step_data.shape)
print("Labels length: ", len(single_step_labels))
# ...

# Sprawdzenie czy dane i etykiety zostały dopełnione zerami
if single_step_data.shape[1] < 22 or len(single_step_labels) < 22:
    print("Ostatnia para danych lub etykiet nie została dopełniona do 22 kroków czasowych.")
else:
    print("Ostatnia para danych i etykiet została poprawnie dopełniona do 22 kroków czasowych.")


split_ratio = 0.8  # 80% danych na trening, 20% na walidację
split_index = int(len(file_data_label_pairs) * split_ratio)

train_data_label_pairs = file_data_label_pairs[:split_index]
validation_data_label_pairs = file_data_label_pairs[split_index:]

print("Liczba par danych treningowych:", len(train_data_label_pairs))
print("Liczba par danych walidacyjnych:", len(validation_data_label_pairs))

# Przygotowanie generatorów
# train_generator = batch_generator(train_data_label_pairs)
# validation_generator = batch_generator(validation_data_label_pairs)

print("Liczba par danych i etykiet:", len(train_data_label_pairs))
""""
for data, labels in train_generator:
    print("Shape danych:", data.shape)
    print("Shape etykiet:", labels.shape)
    break

num_epochs = 10  # Zdefiniuj liczbę epok

# Pętla treningowa
for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}/{num_epochs}")

    # Trening na danych treningowych
    for train_data, train_labels in train_generator:
        model.train_on_batch(train_data, train_labels)

    # Walidacja na danych walidacyjnych
    validation_loss, validation_accuracy = 0, 0
    for validation_data, validation_labels in validation_generator:
        loss, accuracy = model.evaluate(validation_data, validation_labels, verbose=0)
        validation_loss += loss
        validation_accuracy += accuracy

    # Wyświetlenie średnich wyników walidacji
    validation_loss /= len(validation_data_label_pairs)
    validation_accuracy /= len(validation_data_label_pairs)
    print(f"Validation loss: {validation_loss}, Validation accuracy: {validation_accuracy}")
"""