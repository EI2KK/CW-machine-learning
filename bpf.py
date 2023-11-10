import os
import json
import numpy as np
import scipy.signal
import wave
import random

def apply_bandpass_filter(file_path, low_freq, high_freq, framerate, filter_type, order=4, ripple=None, attenuation=None):
    nyquist = 0.5 * framerate
    low = low_freq / nyquist
    high = high_freq / nyquist

    # Read the audio signal
    with wave.open(file_path, 'r') as wav_file:
        nchannels, sampwidth, framerate, nframes, comptype, compname = wav_file.getparams()
        frames = wav_file.readframes(nframes)
        audio_signal = np.frombuffer(frames, dtype=np.int16)

    # Choose the filter and its parameters
    if filter_type == 'butter':
        b, a = scipy.signal.butter(order, [low, high], btype='band')
    elif filter_type == 'cheby1':
        if ripple is None:
            raise ValueError("Parameter 'ripple' must be provided for Chebyshev Type I filter")
        b, a = scipy.signal.cheby1(order, ripple, [low, high], btype='band')
    elif filter_type == 'cheby2':
        if ripple is None:
            raise ValueError("Parameter 'ripple' must be provided for Chebyshev Type II filter")
        b, a = scipy.signal.cheby2(order, ripple, [low, high], btype='band')
    elif filter_type == 'ellip':
        if ripple is None or attenuation is None:
            raise ValueError("Parameters 'ripple' and 'attenuation' must be provided for the Elliptic filter")
        b, a = scipy.signal.ellip(order, ripple, attenuation, [low, high], btype='band')
    else:
        raise ValueError(f"Unsupported filter type: {filter_type}")

    # Filter the signal
    filtered_signal = scipy.signal.lfilter(b, a, audio_signal)
    return filtered_signal, (nchannels, sampwidth, framerate, nframes, comptype, compname)

# Rest of the code remains unchanged

# BPF filter parameters
low_freq = 900  # Lower cutoff frequency
high_freq = 1200  # Upper cutoff frequency

# Filter type and its parameters
# filter_type = 'cheby1'  # 'butter', 'cheby1', 'cheby2', 'ellip'
filter_order = 5
filter_ripple = 0.01  # Only for Chebyshev and Elliptic filters
filter_attenuation = 60  # Only for the Elliptic filter

# Folder paths
input_folder = 'json_folder'
output_folder = 'cw_audio_bpf'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process all .wav files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.wav'):
        file_path = os.path.join(input_folder, file_name)

        # Read 'framerate' from the file
        with wave.open(file_path, 'r') as wav_file:
            framerate = wav_file.getframerate()

        available_filter_types = ['butter', 'cheby1', 'cheby2', 'ellip']
        filter_type = random.choice(available_filter_types)
        
        # Apply the BPF filter
        filtered_signal, params = apply_bandpass_filter(
            file_path, 
            low_freq, 
            high_freq, 
            framerate,
            filter_type=filter_type,
            order=filter_order,
            ripple=filter_ripple, 
            attenuation=filter_attenuation
        )

        # Save the filtered signal to a new WAV file
        output_file_path = os.path.join(output_folder, f'bpf_{file_name}')
        with wave.open(output_file_path, 'w') as wav_file:
            wav_file.setparams(params)
            wav_file.writeframes(filtered_signal.astype(np.int16).tobytes())

        # Read and update the JSON file
        base_name = os.path.splitext(file_name)[0]
        json_file_name = f"label_{base_name.split('_')[-1]}.json"
        json_path = os.path.join(input_folder, json_file_name)

        if os.path.isfile(json_path):
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

            # Update data with low_freq and high_freq
            bpf_params = {
                'low_freq': low_freq,
                'high_freq': high_freq,
                'filter_type': filter_type,
                'filter_ripple': filter_ripple,
                'filter_attenuation': filter_attenuation,
                'filter_order': filter_order
            }

            data['bpf'] = bpf_params

            # Save the modified JSON file
            output_json_path = os.path.join(output_folder, f'bpf_{json_file_name}')
            with open(output_json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

print("Processing completed.")
