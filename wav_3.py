import numpy as np
import wave
import json
import os

# Morse code for characters
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ',': '--..--',
    '.': '.-.-.-', '+': '.-.-.', '!': '-.-.--', ' ': ' ',
}

sample_rate = 44100
inaccuracy=20 
frequency_inaccuracy=0
# Folder containing JSON files
json_directory = 'json_folder'

import numpy as np



def generate_cw_signal(characters, speeds_wpm, frequencies, start_times_ms, file_duration_ms, amplitude=0.5, sample_rate=44100, inaccuracy=0, frequency_inaccuracy=0):
    total_length = int(sample_rate * file_duration_ms / 1000)
    main_signal = np.zeros(total_length)

    for character, speed_wpm, frequency, start_time_ms in zip(characters, speeds_wpm, frequencies, start_times_ms):
        dot_duration = 1200 / speed_wpm  # Duration of one dot (ms)
        dot_length = int(sample_rate * dot_duration / 1000)  # Length of a dot in samples
        dash_length = dot_length * 3
        space_length = dot_length * 7  # Length of space in samples

        char_signal = np.array([])
        if character == ' ':
            # Add a space
            space_signal = np.zeros(space_length)
            char_signal = np.concatenate([char_signal, space_signal])
        elif character.upper() in morse_code:  # Assuming morse_code is a predefined dictionary
            morse_sequence = morse_code[character.upper()]
            for symbol in morse_sequence:
                # Calculate inaccuracy factors
                inaccuracy_factor = 1.0
                if inaccuracy > 0:
                    inaccuracy_percent = np.random.uniform(-inaccuracy, inaccuracy)
                    inaccuracy_factor = 1.0 + (inaccuracy_percent / 100)

                frequency_factor = 1.0
                if frequency_inaccuracy > 0:
                    frequency_percent = np.random.uniform(-frequency_inaccuracy, frequency_inaccuracy)
                    frequency_factor = 1.0 + (frequency_percent / 100)

                if symbol == '.':
                    dot_duration_inaccurate = dot_duration * inaccuracy_factor
                    dot_length_inaccurate = int(sample_rate * dot_duration_inaccurate / 1000)
                    dot_signal = np.sin(2 * np.pi * frequency * frequency_factor * np.linspace(0, dot_duration_inaccurate / 1000, dot_length_inaccurate))
                    char_signal = np.concatenate([char_signal, dot_signal])
                elif symbol == '-':
                    dash_duration_inaccurate = 3 * dot_duration * inaccuracy_factor
                    dash_length_inaccurate = int(sample_rate * dash_duration_inaccurate / 1000)
                    dash_signal = np.sin(2 * np.pi * frequency * frequency_factor * np.linspace(0, dash_duration_inaccurate / 1000, dash_length_inaccurate))
                    char_signal = np.concatenate([char_signal, dash_signal])

                # Add a pause after each symbol
                silence = np.zeros(dot_length)
                char_signal = np.concatenate([char_signal, silence])

        # Normalize the character signal to the specified amplitude only if it's not all zeros
        if len(char_signal) > 0 and np.max(np.abs(char_signal)) != 0:
            char_signal = amplitude * char_signal / np.max(np.abs(char_signal))

        # Mix the character signal with the main signal
        start_sample = int(sample_rate * start_time_ms / 1000)
        end_sample = min(start_sample + len(char_signal), total_length)
        main_signal[start_sample:end_sample] += char_signal[:end_sample - start_sample]

    return main_signal





# Process all JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        json_path = os.path.join(json_directory, filename)

        with open(json_path, 'r') as file:
            data = json.load(file)

        #sample_rate = 44100  # Constant sample_rate value if not available in JSON

        # Generate a signal based on JSON data
        cw_signal = generate_cw_signal(
            data['cw_text'],
            data['speed_wpm'],
            data['frequency'],
            data['start_time_ms'],
            data['file_duration_ms'],  # Make sure this is a single value
            sample_rate=sample_rate,
            inaccuracy=inaccuracy,
            frequency_inaccuracy=frequency_inaccuracy
        )
        
        # Number of samples in the signal
        num_samples = len(cw_signal)
        
        # Save the audio file
        wave_file_path = os.path.join(json_directory, data['file_name'])
        with wave.open(wave_file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)  # Make sure this line is before wf.writeframes
            wf.writeframes((cw_signal * 32767).astype(np.int16).tobytes())

        # Add additional information to the JSON file
        data['sample_rate'] = sample_rate
        data['num_samples'] = num_samples

        # Save the modified JSON file
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)

print(f"Done, WAV files have been created.")
