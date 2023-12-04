import numpy as np
import wave
import os
import random
import json
from concurrent.futures import ThreadPoolExecutor


def add_noise_vectorized(audio_data, block_size, base_snr_in_db, variability_percentage, signal_energy):
    noisy_audio = np.copy(audio_data).astype(np.float64)
    for i in range(0, len(audio_data), block_size):
        snr_variation = base_snr_in_db * (1 + random.uniform(-variability_percentage, variability_percentage) / 100)
        noise_energy = signal_energy / (10 ** (snr_variation / 10))
        noise = np.random.normal(scale=np.sqrt(noise_energy), size=min(block_size, len(audio_data) - i))
        noisy_audio[i:i + block_size] += noise
    return np.clip(noisy_audio, -32768, 32767).astype(np.int16)


def process_file(file_path, snr_range, variability_percentage):
    with wave.open(file_path, 'rb') as audio:
        num_frames = audio.getnframes()
        sample_width = audio.getsampwidth()
        framerate = audio.getframerate()
        audio_data = np.frombuffer(audio.readframes(num_frames), dtype=np.int16)

    base_snr_in_db = random.uniform(*snr_range)
    if base_snr_in_db < 0:
        gain = 1 + (base_snr_in_db / 100)
        audio_data = audio_data.astype(np.float64)
        audio_data *= gain
        audio_data = audio_data.astype(np.int16)

    signal_energy = np.mean(np.square(audio_data.astype(np.float64)))
    block_size = 1024
    noisy_audio = add_noise_vectorized(audio_data, block_size, base_snr_in_db, variability_percentage, signal_energy)

    with wave.open(file_path, 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(sample_width)
        output.setframerate(framerate)
        output.writeframes(noisy_audio.tobytes())

    return file_path, signal_energy, base_snr_in_db



def add_variable_noise_to_audio(input_folder, snr_range, variability_percentage):
    file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".wav")]

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda f: process_file(f, snr_range, variability_percentage), file_paths)

        for file_path, signal_energy, base_snr_in_db in results:
            label = int(os.path.basename(file_path).split("_")[-1].split(".")[0])
            print(f"{os.path.basename(file_path)}", end='\r')

            json_filename = os.path.join(input_folder, f'cw_{label:05}.json')
            if os.path.exists(json_filename):
                with open(json_filename, 'r') as json_file:
                    json_data = json.load(json_file)

                json_data["S/N (dB)"] = round(10 * np.log10(signal_energy / (signal_energy / (10 ** (base_snr_in_db / 10)))), 2)

                with open(json_filename, 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)



add_variable_noise_to_audio(input_folder, (-5, -1), 10) # (zakres), zmiennosc w %)
