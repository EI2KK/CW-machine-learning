import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import glob
import os

if __name__ == '__main__':
    wav_directory = 'json_folder_001_014'



def plot_spectrogram(wav_file, freq_min, freq_max):
    sample_rate, audio = wavfile.read(wav_file)
    
    if audio.ndim > 1:
        audio = audio[:, 0]

    frequencies, times, Sxx = spectrogram(audio, fs=sample_rate, # window='hann', 
                                      nperseg=2048, noverlap=1607)
                                      
                                      
    idx_min = np.argmax(frequencies > freq_min) - 1
    idx_max = np.argmax(frequencies > freq_max) - 1
    frequencies = frequencies[idx_min:idx_max]
    Sxx = Sxx[idx_min:idx_max, :]
 
    epsilon = 1e-10 
    real_spectrogram_data_db =  10 * np.log10(np.abs(Sxx) + epsilon)
    threshold_db = 30
    real_spectrogram_data_db -= threshold_db

    npy_file = os.path.splitext(wav_file)[0] + '.npy'
    np.save(npy_file, real_spectrogram_data_db)                         

wav_files = glob.glob(os.path.join(wav_directory, '*.wav'))

for wav_file in wav_files:
    freq_min = 300 
    freq_max = 1000
    print(f"{os.path.basename(wav_file)}", end='\r')
    plot_spectrogram(wav_file, freq_min, freq_max)
