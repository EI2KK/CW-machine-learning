import numpy as np
from scipy.signal import spectrogram


sample_rate = 48000
freq_min = 300
freq_max = 1000
nperseg = 4800
noverlap =  nperseg - (sample_rate * 0.005) #3616



audio_length = sample_rate * 5
audio = np.random.normal(0, 1, audio_length)

frequencies, times, Sxx = spectrogram(audio, fs=sample_rate, nperseg=nperseg, noverlap=noverlap)

idx_min = np.argmax(frequencies > freq_min) - 1
idx_max = np.argmax(frequencies > freq_max) - 1

num_features = idx_max - idx_min


time_step_ms = ((nperseg - noverlap) / sample_rate) * 1000
print(nperseg, noverlap)
print(num_features, ' features, time-step = ', time_step_ms,'ms')
print((freq_max - freq_min)/num_features)
"""
sample_rate = 44100  
freq_min = 600      
freq_max = 800      
nperseg = 8192
noverlap = 7751

37  features, time-step =  10.0 ms

"""