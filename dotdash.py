import random
import json
import os
import time
import numpy as np
import shutil

script_start_time = time.time()
print("JSON")

characters = "ETANIMSOUDKRGWHBCFJLPQVXYZ0123456789?!/"
character_list = list(characters)
num_files_to_generate = 10
training = 1
batch = 14
n = 6  # number of characters used 
char_range = (2, 5)
speed_range = (18, 25)
freq_range = (300, 1000)
min_sep = 30
qrm_sep = 30
sidetone = 700
start_between_ms = (50, 300)
stop_b4_end = 1800 # must be grater than pause_length
nr_of_freq = 2
nr_of_qrm_freq = 1
qrm_length = (800, 24000)  # max length must be less than total_length
qrm_start_between = (300, 1000)
min_volume = 0.35
pause_probablilty = 35
pause_length = 1600
total_length = 30000
noise = True


json_directory_ = 'json_folder'

def sec_to_hhmmss(sec):
    sec = int(sec)  
    hr, rem = divmod(sec, 3600)
    minuts, sec = divmod(rem, 60)
    return "{:02}:{:02}:{:02}".format(hr, minuts, sec)

formatted_training = f"{training:03}" 
formatted_batch = f"{batch:03}" 

json_file_name = 'training.json'

json_directory = f"{json_directory_}_{formatted_training}_{formatted_batch}"

# Struktura danych do zapisania
character_list_string = ','.join(character_list[:n])
data_to_save = {
    'model':[],
    'training': formatted_training,
    'batch': formatted_batch,
    'audio_length': sec_to_hhmmss(num_files_to_generate * total_length / 1000),
    'directory': json_directory,
    'characters': n,
    'character_list': character_list_string
    }


if os.path.exists(json_file_name):
    with open(json_file_name, 'r') as file:
        data = json.load(file)
   

    entry_found = False
    for entry in data:
        if entry['training'] == formatted_training and entry['batch'] == formatted_batch:
            entry.update(data_to_save)
            entry_found = True
            break

    if not entry_found:
        data.append(data_to_save)
else:
    data = [data_to_save]


with open(json_file_name, 'w') as file:
    json.dump(data, file, indent=4)

directory_name = f"{json_directory_}_{training:03}_{batch:03}"
os.makedirs(directory_name, exist_ok=True)

# Morse code mapping dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '/': '-..-.', '!': '-.-.--', '?': '..--..', ' ': ' '
}


def generate_morse_data(char, start_time, speed, max_end_time):
    unit_duration = 1200 / speed  # Czas trwania pojedynczego dot
    data = []
    morse_elements = morse_code[char]

    for index, element in enumerate(morse_elements):
        next_time = start_time + (unit_duration if element == '.' else 3 * unit_duration)
        if next_time > max_end_time:
            break
        data.append({"element": "dot" if element == '.' else "dash", "start_ms": start_time, "end_ms": next_time, "duration_ms": next_time - start_time})
        start_time = next_time
        element_end = False
        element_gap = start_time + unit_duration
        if element_gap > max_end_time:
            break
        
        data.append({"element": "element_end", "start_ms": start_time, "end_ms": start_time + unit_duration, "duration_ms": unit_duration})
        start_time = element_gap
    
    data.append({"element": "char_end", "start_ms": start_time, "end_ms": start_time + (3 * unit_duration), "duration_ms": (3 * unit_duration)})

    return data, start_time


def generate_word_data(word, start_time, speed, max_end_time):
    data = []
    for char in word:
        char_data, start_time = generate_morse_data(char, start_time, speed, max_end_time)
        if not char_data:
            break
        data.extend(char_data)
        char_end_time = start_time + 3 * 1200 / speed
        word_start_time = start_time
        if char_end_time <= max_end_time:
            start_time = char_end_time
        else:
            break

    word_end_time = word_start_time + 7 * 1200 / speed
    
    if word_end_time > (total_length - stop_b4_end):
        data.append({"element": "word_end", "start_ms": word_start_time, "end_ms": word_end_time, "duration_ms": word_end_time - word_start_time})
        data.append({"element": "pause", "start_ms": word_start_time, "end_ms": word_start_time + pause_length, "duration_ms": pause_length})
        
    if word_end_time <= max_end_time:
        data.append({"element": "word_end", "start_ms": word_start_time, "end_ms": word_end_time, "duration_ms": word_end_time - word_start_time})
        
        if (max_end_time - word_start_time) > pause_length:
                x = random.randint(1, 100)
                if x <= pause_probablilty:
                    word_end_time = word_start_time + pause_length
                    data.append({"element": "pause", "start_ms": word_start_time, "end_ms": word_end_time, "duration_ms": pause_length})
        
        
    start_time = word_end_time
    return data, start_time


def generate_frequencies(nr_of_freq, freq_range, min_sep):
    possible_frequencies = set(range(freq_range[0], freq_range[1] + 1))
    frequencies = []

    while len(frequencies) < nr_of_freq and possible_frequencies:
        frequency = random.choice(list(possible_frequencies))
        frequencies.append(frequency)

        for freq in range(frequency - min_sep, frequency + min_sep + 1):
            possible_frequencies.discard(freq)

    return sorted(frequencies)
    
def generate_qrm_frequencies(nr_of_qrm_freq, freq_range, min_sep, frequencies):
    possible_qrm_frequencies = set(range(freq_range[0], freq_range[1] + 1))

    for freq in frequencies:
        for near_freq in range(freq - min_sep, freq + min_sep + 1):
            possible_qrm_frequencies.discard(near_freq)

    qrm_frequencies = []

    while len(qrm_frequencies) < nr_of_qrm_freq and possible_qrm_frequencies:
        qrm_frequency = random.choice(list(possible_qrm_frequencies))
        qrm_frequencies.append(qrm_frequency)

    return sorted(qrm_frequencies)    

for file_number in range(1, num_files_to_generate + 1):

    json_data = {
        "cw_file": f"cw_{file_number:05}.wav",
        "npy_file": f"cw_{file_number:05}.npy",
        "session_duration_ms": total_length, 
        "noise": noise,
        "S/N (dB)": None,
        "speed_range": speed_range,
        "freq_range": freq_range,
        "start_between_ms": start_between_ms,
        "stop_b4_end": stop_b4_end,
        "nr_of_freq": nr_of_freq, 
        "training": training,
        "batch": batch,
        "elements": []
        }
    frequencies = []
    frequencies = generate_frequencies(nr_of_freq, freq_range, min_sep)
    qrm_frequencies = generate_qrm_frequencies(nr_of_qrm_freq, freq_range, qrm_sep, frequencies)
    
        
    for _ in range(nr_of_freq):
    
        frequency = frequencies[_]
        speed = random.randint(*speed_range)
        start_time = random.randint(*start_between_ms)
        volume = round(random.uniform(min_volume, 1), 3)
        freq_data = {"frequency": frequency, "speed_wpm": speed, "output": 0, "volume": volume, "data": []}  # Dodano 'volume'
    
        limited_character_list = character_list[:n]

        while start_time < total_length - stop_b4_end:
            word_length = random.randint(*char_range)
            word = ''.join(random.choices(limited_character_list, k=word_length))
            word_data, new_start_time = generate_word_data(word, start_time, speed, total_length - stop_b4_end)
            if new_start_time == start_time:
                break
            start_time = new_start_time
            freq_data["data"].extend(word_data)

        json_data["elements"].append(freq_data)

    # QRM    
    for _ in range(nr_of_qrm_freq):
        frequency = qrm_frequencies[_]
        volume = round(random.uniform(min_volume, 1), 3)
        qrm_data = {"frequency": frequency, "speed_wpm": 0, "output": 0, "volume": volume, "data": []}  # Dodano 'volume'
        
        start_time = random.randint(*qrm_start_between)
        qrm_duration = random.randint(*qrm_length)
        
        if (start_time + qrm_duration) > total_length:
            qrm_duration = total_length - start_time - 1
        
        data = []
        data.append({"element": "qrm", "start_ms": start_time, "end_ms": start_time + qrm_duration, "duration_ms": qrm_duration})
        
        
        if (1.8 * (start_time + qrm_duration)) < total_length:
            start_time = (start_time + qrm_duration) + random.randint(300, 1200)
            volume = round(random.uniform(min_volume, 1), 3)
            qrm_duration = random.randint(*qrm_length)
            data.append({"element": "qrm", "start_ms": start_time, "end_ms": start_time + qrm_duration, "duration_ms": qrm_duration})
            qrm_data["data"].extend(data)
        
        json_data["elements"].append(qrm_data)    
    
    file_name = f"cw_{file_number:05}.json"
    file_path = os.path.join(directory_name, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)




elapsed_time = round(time.time() - script_start_time, 2)
print(f"        :{elapsed_time}s.   ")
step_time = time.time()

print("WAV")
with open('wav_dd.py', 'r') as file:
    code = file.read()
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    exec(code, {'directory': parametr})
    elapsed_time = round(time.time() - step_time, 2)
    step_time = time.time()
    print(f"        :{elapsed_time}s.   ")
    

if noise:
    print("NOISE")
    with open('noise_bulk.py', 'r') as file:
        code = file.read()
        parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
        exec(code, {'input_folder': parametr})
        elapsed_time = round(time.time() - step_time, 2)
        step_time = time.time()
        print(f"        :{elapsed_time}s.   ")
    
print("FFT")    
with open('fftg.py', 'r') as file:
    code = file.read()
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    exec(code, {'wav_directory': parametr})
    elapsed_time = round(time.time() - step_time, 2)
    step_time = time.time()
    print(f"        :{elapsed_time}s.   ")
    
print("LABEL")
with open('label_npy.py', 'r') as file:
    code = file.read()
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    exec(code, {'directory': parametr})
    elapsed_time = round(time.time() - step_time, 2)
    step_time = time.time()
    print(f"        :{elapsed_time}s.   ")
    

print("Removing .vav and .json files...")
def delete_files(directory, extensions):
    for item in os.listdir(directory):
        if item.endswith(extensions):
            os.remove(os.path.join(directory, item))

delete_files(json_directory, ('.wav', '.json'))

elapsed_time = round(time.time() - step_time, 2)
step_time = time.time()
print(f"        :{elapsed_time}s.   ")

def split_data(source_directory, train_ratio=0.8):
    # Utwórz ścieżki do podkatalogów
    train_directory = os.path.join(source_directory, 'training')
    validation_directory = os.path.join(source_directory, 'validation')

    # Utwórz podkatalogi, jeśli nie istnieją
    os.makedirs(train_directory, exist_ok=True)
    os.makedirs(validation_directory, exist_ok=True)

    # Wczytaj wszystkie pliki .npy
    all_files = [f for f in os.listdir(source_directory) if f.endswith('.npy')]

    # Losowe mieszanie plików
    np.random.shuffle(all_files)

    # Podział plików na treningowe i walidacyjne
    split_index = int(len(all_files) * train_ratio)
    train_files = all_files[:split_index]
    validation_files = all_files[split_index:]

    # Przenieś pliki do odpowiednich podkatalogów
    for f in train_files:
        shutil.move(os.path.join(source_directory, f), train_directory)

    for f in validation_files:
        shutil.move(os.path.join(source_directory, f), validation_directory)

split_data(json_directory, train_ratio=0.8)

elapsed_time = round(time.time() - script_start_time, 2)
print(f"Total execution time: {elapsed_time}s.  ")
print(f"Total length of audio data : {sec_to_hhmmss(num_files_to_generate * total_length / 1000)}")