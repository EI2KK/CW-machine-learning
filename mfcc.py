import librosa
import numpy as np
import json
import os
import time

start_time = time.time()

# Parametry MFCC
n_mfcc = 20
n_fft = 512
hop_length = 256
win_length = 512
n_mels = 95
fmax = 22050
precision = 2

# Wczytanie pliku training.json
with open('training.json', 'r') as file:
    training_data = json.load(file)

for record in training_data:
    if not record['mfcc']:
        folder_path = record['json_directory']

        # Iterowanie przez pliki w folderze
        for filename in os.listdir(folder_path):
            if filename.endswith('.wav'):
                # Ścieżki do plików WAV i JSON
                wav_path = os.path.join(folder_path, filename)
                json_path = os.path.join(folder_path, filename.replace('cw_', 'label_').replace('.wav', '.json'))
                mfcc_filename = filename.replace('.wav', '.npy')

                # Wczytywanie pliku audio
                audio, sample_rate = librosa.load(wav_path, sr=None)

                # Ekstrakcja MFCC
                mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length, win_length=win_length, n_mels=n_mels, fmax=fmax)

                # Zapis MFCC do pliku .npy
                npy_path = wav_path.replace('.wav', '.npy')
                np.save(npy_path, mfcc)

                # Usunięcie pliku .wav
                os.remove(wav_path)

                # Aktualizacja pliku JSON
                if os.path.exists(json_path):
                    with open(json_path, 'r') as json_file:
                        data = json.load(json_file)

                    # Aktualizacja nazwy pliku
                    data['file_name'] = mfcc_filename

                    # Dodawanie informacji o MFCC
                    data['mfcc_params'] = {
                        'n_mfcc': n_mfcc,
                        'n_fft': n_fft,
                        'hop_length': hop_length,
                        'win_length': win_length,
                        'n_mels': n_mels,
                        'fmax': fmax 
                    }

                    # Obliczanie i dodawanie mfcc_time_frames
                    num_frames = mfcc.shape[1]
                    frame_duration = hop_length / sample_rate * 1000  # Czas trwania jednej ramki w milisekundach
                    mfcc_time_frames = [round(frame_duration * i, precision) for i in range(num_frames)]

                    data['mfcc_time_frames'] = mfcc_time_frames

                    # Zapisanie zaktualizowanych danych do pliku JSON
                    with open(json_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)
        
        # Ustawienie 'mfcc' na true po przetworzeniu plików
        record['mfcc'] = True

# Zapisanie zmodyfikowanego training.json
with open('training.json', 'w') as file:
    json.dump(training_data, file, indent=4)

elapsed_time = round(time.time() - start_time, 2)
print(f"Czas wykonania skryptu: {elapsed_time} sekund.")
