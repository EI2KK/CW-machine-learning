import numpy as np
import matplotlib.pyplot as plt
import os

# Ścieżka do katalogu z plikami .npy
folder_path = 'json_folder_001_004'  # Zmodyfikuj tę ścieżkę zgodnie z potrzebami

# Listowanie wszystkich plików .npy w podanym katalogu
npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]

# Iteracja po wszystkich plikach .npy
for file in npy_files:
    # Wczytywanie danych z pliku .npy
    spectrogram_data = np.load(os.path.join(folder_path, file))

    # Limitowanie zakresu wyświetlanych danych spektrogramu
    limited_spectrogram_data = spectrogram_data

    # Wyświetlanie wykresu
    plt.figure(figsize=(12, 6))
    plt.imshow(limited_spectrogram_data, cmap='viridis', origin='lower', aspect='auto')
    plt.ylabel('Częstotliwość [Hz]')
    plt.xlabel('Czas [indeksy próbek]')
    plt.title(f'Ograniczony zakres częstotliwości spektrogramu - {file}')
    plt.colorbar(format='%+2.0f dB')

    # Non-blocking show and wait for a button press or window close event
    plt.show(block=False)
    plt.waitforbuttonpress()
    plt.close()  # Zamykanie aktywnego okna wykresu
