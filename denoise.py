import numpy as np
import os
import time 

# Ścieżka do katalogu z plikami .npy
directory = 'json_folder_001_014'

def calculate_snr(spectrogram_path):
    """
    Oblicza stosunek sygnał-szum (SNR) dla spektrogramu zapisanego w pliku .npy.
    
    :param spectrogram_path: Ścieżka do pliku .npy zawierającego spektrogram.
    :return: SNR w decybelach (dB).
    """
    # Wczytywanie spektrogramu
    spectrogram = np.load(spectrogram_path)

    # Definiowanie zakresów sygnału i szumu
    noise_region = spectrogram[:, -50:]  # Zakładamy, że ostatnie 50 kroków to szum
    signal_region = spectrogram[:, :-50]  # Reszta to sygnał

    # Obliczanie mocy sygnału i szumu
    power_signal = np.mean(signal_region**2)
    power_noise = np.mean(noise_region**2)

    # Obliczanie SNR
    SNR = 10 * np.log10(power_signal / power_noise) if power_noise != 0 else float('inf')

    return SNR


def load_spectrograms(directory):
    spectrograms = []
    file_names = []
    for file in os.listdir(directory):
        if file.startswith("cw") and file.endswith(".npy"):
            path = os.path.join(directory, file)
            spectrogram = np.load(path)
            spectrograms.append(spectrogram)
            file_names.append(file)
    return spectrograms, file_names

def analyze_noise(spectrograms):
    noise_profiles = []
    for spec in spectrograms:
        if spec.shape[1] >= 50:  # Sprawdzanie czy mamy przynajmniej 50 kroków czasowych
            noise = spec[:, -50:]  # Ostatnie 50 kroków
            noise_profile = np.mean(noise, axis=1)  # Średnia po krokach czasowych
            noise_profiles.append(noise_profile)
        else:
            noise_profiles.append(None)
    return noise_profiles

def remove_noise_and_save(spectrograms, noise_profiles, file_names, directory, noise_reduction_factor=1.0):
    for spec, noise_profile, file_name in zip(spectrograms, noise_profiles, file_names):
        if noise_profile is not None:
            # Kontrola agresywności usuwania szumu
            adjusted_noise_profile = noise_profile * noise_reduction_factor
            denoised_spec = spec - adjusted_noise_profile[:, None]
        else:
            denoised_spec = spec

        new_file_name = "clean_" + file_name
        save_path = os.path.join(directory, new_file_name)
        np.save(save_path, denoised_spec)

# Wartość `noise_reduction_factor` kontroluje, jak bardzo redukowany jest szum
# 1.0 oznacza pełne usuwanie szumu zgodnie z profilem, mniejsze wartości będą mniej agresywne
noise_reduction_factor = 1  # Możesz dostosować tę wartość




# Wczytanie spektrogramów
spectrograms, file_names = load_spectrograms(directory)

# Analiza szumu
noise_profiles = analyze_noise(spectrograms)

# Usuwanie szumu i zapisywanie
remove_noise_and_save(spectrograms, noise_profiles, file_names, directory, noise_reduction_factor)

time.sleep(2)



# Przykład użycia

snr = calculate_snr('json_folder_001_014/cw_00001.npy')
print(f'SNR: {snr} dB')
snr = calculate_snr('json_folder_001_014/clean_cw_00001.npy')
print(f'SNR: {snr} dB')