import os
import wave
import random
import numpy as np
import json
from shutil import copyfile
import time
import os
import wave
import numpy as np
import random

if __name__ == '__main__':
    input_folder = 'json_folder'

output_folder = input_folder

start_time = time.time()

def add_variable_noise_to_audio(input_folder, snr_range, variability_percentage):
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)
            label = int(filename.split("_")[-1].split(".")[0])

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
            noisy_audio = np.copy(audio_data)

            for i in range(0, len(audio_data), block_size):
                snr_variation = base_snr_in_db * (1 + random.uniform(-variability_percentage, variability_percentage) / 100)
                noise_energy = signal_energy / (10 ** (snr_variation / 10))

                for j in range(i, min(i + block_size, len(audio_data))):
                    noise_sample = np.random.normal(scale=np.sqrt(noise_energy))
                    noisy_sample = audio_data[j] + noise_sample
                    noisy_audio[j] = np.clip(noisy_sample, -32768, 32767) if not np.isnan(noisy_sample) else 0

            with wave.open(file_path, 'wb') as output:
                output.setnchannels(1)
                output.setsampwidth(sample_width)
                output.setframerate(framerate)
                output.writeframes(noisy_audio.tobytes())

            json_filename = os.path.join(input_folder, f'label_{label:05}.json')
            if os.path.exists(json_filename):
                with open(json_filename, 'r') as json_file:
                    json_data = json.load(json_file)

                json_data["S/N (dB)"] = round(10 * np.log10(signal_energy / noise_energy), 2) if not np.isnan(noise_energy) and noise_energy > 0 else 0

                with open(json_filename, 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)
    



add_variable_noise_to_audio(input_folder, (-5, 0), 10) # (zakres), zmiennosc w %)
elapsed_time = round(time.time() - start_time, 2)
print(f"Czas wykonania skryptu: {elapsed_time} sekund.")