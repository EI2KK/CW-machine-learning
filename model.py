import os
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Attention, Input
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.models import Model
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ModelCheckpoint
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
## resetowanie stanu pomiedzy plikami model.reset_states()
## dodanie wymiaru do sekwencji dane = np.expand_dims(dane, axis=0)
input_layer = Input(batch_shape=(1, 22, 33))

# Tworzenie warstwy wejściowej

# Dodawanie warstw LSTM
lstm_layer = LSTM(lstm_units, return_sequences=True, stateful=True)(input_layer)
lstm_layer = LSTM(lstm_units, return_sequences=True, stateful=True)(lstm_layer)

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


model_id = "01.01"
# Otwieranie pliku JSON i wczytywanie danych
with open('training.json', 'r') as file:
    data = json.load(file)

# Szukanie pierwszego rekordu bez danego model_id
for record in data:
    if model_id not in record.get("model", []):
        directory = record["directory"]
        break
data_folder = os.path.join(directory)
split_data(data_folder, train_ratio=0.8)

# Użycie funkcji
# data_folder = 'json_folder_001_014'
# all_training_data = load_and_process_data(data_folder)

# train_percent = 0.8

# Mieszanie danych
# random.shuffle(all_training_data)

# Określenie liczby plików do treningu
# num_train_files = int(len(all_training_data) * train_percent)

# Podział na dane treningowe i walidacyjne
train_data = load_and_process_data(os.path.join(data_folder, "training")) # all_training_data[:num_train_files]
validation_data = load_and_process_data(os.path.join(data_folder, "validation")) #  all_training_data[num_train_files:]

num_epochs = 10  # Liczba epok treningu
best_val_accuracy = 0  # Najlepsza dokładność walidacji
no_improvement_epochs = 0  # Licznik epok bez poprawy
early_stopping_threshold = 3  # Liczba epok bez poprawy, po której następuje przerwanie treningu

# Przygotowanie callbacków
# early_stopping = EarlyStopping(monitor='val_accuracy', patience=early_stopping_threshold)
# model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True)

for epoch in range(num_epochs):
    print(f"Epoka {epoch+1}/{num_epochs}")

 # Trening modelu
    for file_data in train_data:
        for sequence in file_data["file"][0]["sequence"]:
            X = sequence["data"]  # Dane wejściowe z sekwencji
            y = prepare_labels(sequence["labels"])  # Przetwarzanie etykiet dla sekwencji
            model.train_on_batch(X, y)

    # Walidacja modelu
    total_validation_loss = 0
    total_validation_accuracy = 0
    num_batches = 0

    for file_data in validation_data:
        for sequence in file_data["file"][0]["sequence"]:
            X_val = sequence["data"]  # Dane wejściowe z sekwencji dla walidacji
            y_val = prepare_labels(sequence["labels"])  # Przetwarzanie etykiet dla sekwencji
            validation_results = model.evaluate(X_val, y_val, verbose=0)
            
            total_validation_loss += validation_results[0]
            total_validation_accuracy += validation_results[1]
            num_batches += 1

    # Obliczenie średniej straty i dokładności na danych walidacyjnych
    average_validation_loss = total_validation_loss / num_batches
    average_validation_accuracy = total_validation_accuracy / num_batches
   
    # Sprawdzenie, czy dokładność walidacji się poprawiła
    if average_validation_accuracy > best_val_accuracy:
        best_val_accuracy = average_validation_accuracy
        no_improvement_epochs = 0
        model.save('best_model.h5')  # Zapis najlepszego modelu
    else:
        no_improvement_epochs += 1

    if no_improvement_epochs >= early_stopping_threshold:
        print("Brak postępu. Przerywanie treningu.")
        break

    print(f"Średnia strata walidacji: {average_validation_loss}")
    print(f"Średnia dokładność walidacji: {average_validation_accuracy}")

# Załadowanie najlepszego modelu
model = keras.models.load_model('best_model.h5')
