import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import glob
import os

if __name__ == '__main__':
    # Ścieżka do katalogu z plikami WAV
    wav_directory = 'json_folder_001_003'



def plot_spectrogram(wav_file, freq_min, freq_max):
    # Wczytanie pliku WAV
    sample_rate, audio = wavfile.read(wav_file)
    
    # Przyjęcie tylko jednego kanału w przypadku plików stereo
    if audio.ndim > 1:
        audio = audio[:, 0]

    # Obliczenie spektrogramu
    frequencies, times, Sxx = spectrogram(audio, fs=sample_rate, window='hann', 
                                      nperseg=2048, noverlap=1024)
                                      
                                      
    # Filtracja w celu uwzględnienia tylko określonego zakresu częstotliwości
    idx_min = np.argmax(frequencies > freq_min) - 1
    idx_max = np.argmax(frequencies > freq_max) - 1
    frequencies = frequencies[idx_min:idx_max]
    Sxx = Sxx[idx_min:idx_max, :]
 
    epsilon = 1e-10 
    # Zapisz tylko część rzeczywistych danych spektrogramu (np. magnitudę)
    real_spectrogram_data_db = 10 * np.log10(np.abs(Sxx) + epsilon)
    threshold_db = 60
    #real_spectrogram_data_db[real_spectrogram_data_db < threshold_db] = 0
    real_spectrogram_data_db -= threshold_db
    # Teraz masz tablicę `real_spectrogram_data` z rzeczywistymi danymi spektrogramu

# Zapisz spektrogram do pliku .npy
    npy_file = os.path.splitext(wav_file)[0] + '.npy'
    np.save(npy_file, real_spectrogram_data_db)                         



    # Wyświetlenie spektrogramu
    #plt.figure(figsize=(12, 6))
    #plt.pcolormesh(times, frequencies, real_spectrogram_data_db, shading='gouraud')
    #plt.ylabel('Częstotliwość [Hz]')
    #plt.xlabel('Czas [sek]')
    #plt.title(npy_file)
    #plt.colorbar(format='%+2.0f dB')
    #plt.ylim(freq_min, freq_max)  # Ograniczenie osi Y do wybranego zakresu częstotliwości
    #plt.show()



# Wyszukaj pliki WAV w katalogu
wav_files = glob.glob(os.path.join(wav_directory, '*.wav'))

# Dla każdego pliku WAV wywołaj funkcję plot_spectrogram
for wav_file in wav_files:
    freq_min = 300  # Dolna granica analizowanego zakresu częstotliwości
    freq_max = 1000  # Górna granica analizowanego zakresu częstotliwości
    print(f"{os.path.basename(wav_file)}", end='\r')
    plot_spectrogram(wav_file, freq_min, freq_max)
"""
freq 300 do 1000
Dla okna 250 ms:    33×11=363 neuronów
Dla okna 500 ms:    33×22=726 neuronów
Dla okna 1000 ms:   33×44=1452 neuronów


Zmiana zakresu częstotliwości na 500-900 Hz powoduje, że liczba pasm częstotliwościowych w spektrogramie wynosi teraz 18. Dla różnych okien czasowych, liczba neuronów w warstwie wejściowej modelu uczenia maszynowego będzie teraz wynosić:

Dla okna 250 ms:    18×11=198 neuronów
Dla okna 500 ms:    18×22=396 neuronów
Dla okna 1000 ms:   18×44=792 neuronów

"""