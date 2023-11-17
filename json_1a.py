import random
import json
import os

characters = "ABC DEFGH IJK LMNO PQRST UVWXYZ 01234 56789 ?!/ "
character_list = list(characters)
speed_range = (25, 25)
min_frequency = 700  
max_frequency = 700  
min_char = 7
max_char = 9
num_files_to_generate = 10
training = 1
batch = 3
json_directory_ = 'json_folder'


## zapis danych o wygenerowanych plikach

json_file_name = 'training.json'

# Formatowanie wartości z wiodącymi zerami
formatted_training = f"{training:03}"  # Formatuje 'training' do postaci trzycyfrowej
formatted_batch = f"{batch:03}"  # Formatuje 'batch' do postaci trzycyfrowej

# Tworzenie nowej nazwy katalogu
json_directory = f"{json_directory_}_{formatted_training}_{formatted_batch}"

# Struktura danych do zapisania
data_to_save = {
    'formatted_training': formatted_training,
    'formatted_batch': formatted_batch,
    'json_directory': json_directory,
    'speed_range': speed_range,
    'min_frequency': min_frequency,
    'max_frequency': max_frequency,
    'min_char': min_char,
    'max_char': max_char,
    'num_of_files': num_files_to_generate,
    'mfcc': False
}

# Sprawdzanie, czy plik JSON już istnieje
if os.path.exists(json_file_name):
    # Odczytywanie istniejących danych
    with open(json_file_name, 'r') as file:
        data = json.load(file)
    
    # Sprawdzanie, czy istnieje wpis z tymi samymi wartościami formatted_training i formatted_batch
    entry_found = False
    for entry in data:
        if entry['formatted_training'] == formatted_training and entry['formatted_batch'] == formatted_batch:
            # Aktualizacja istniejącego wpisu
            entry.update(data_to_save)
            entry_found = True
            break

    if not entry_found:
        # Dodanie nowego wpisu, jeśli nie znaleziono pasującego
        data.append(data_to_save)
else:
    # Utworzenie nowego pliku z pierwszym wpisem
    data = [data_to_save]

# Zapisywanie danych do pliku JSON
with open(json_file_name, 'w') as file:
    json.dump(data, file, indent=4)


if not os.path.exists(json_directory):
    os.makedirs(json_directory)

# Function to generate Morse code text of a given length
def generate_cw_text(length):
    return [random.choice(character_list) for _ in range(length)]

# Morse code mapping dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '/': '-..-.', '!': '-.-.--', '?': '..--..', ' ': ' '
}

# Function to calculate the duration of a Morse code character
def calculate_morse_duration(char, wpm):
    dot_duration_ms = int(1200 / wpm)  
    dash_duration_ms = 3 * dot_duration_ms  
    intra_char_space_ms = dot_duration_ms  

    morse_sequence = morse_code.get(char, '')
    char_duration_ms = 0

    for i, symbol in enumerate(morse_sequence):
        if symbol == '.':
            char_duration_ms += dot_duration_ms
        elif symbol == '-':
            char_duration_ms += dash_duration_ms
        elif symbol == ' ':
            char_duration_ms = 3 * dash_duration_ms
        
        if i < len(morse_sequence) - 1:
            char_duration_ms += intra_char_space_ms

    
    char_duration_ms += 3 * dot_duration_ms

    return char_duration_ms



# Function to find the Morse character with the longest duration
def find_longest_morse_char(wpm):
    longest_duration = 0
    longest_char = None

    for char in morse_code.keys():
        duration_ms = calculate_morse_duration(char, wpm)
        if duration_ms > longest_duration:
            longest_duration = duration_ms
            longest_char = char

    return longest_char, longest_duration
    
wpm_min, wpm_max = speed_range
wpm = wpm_min  
longest_char, longest_duration = find_longest_morse_char(wpm)
file_duration_ms = (max_char + 1) * longest_duration

# Function to generate a JSON file with CW (Morse code) data
def generate_json_file(file_number, cw_text, wpm, frequency):
    file_name = f"cw_{file_number:05}.wav"
    speed_wpm = [wpm for _ in cw_text]  
    frequencies = [frequency for _ in cw_text]  

    duration_ms = [calculate_morse_duration(char, wpm) for char in cw_text]

    total_duration = sum(duration_ms)
    num_chars = len(cw_text)

    start_time_ms = round(random.uniform(700, 1300))
    start_times = []
    for char_duration in duration_ms:
        start_times.append(start_time_ms)
        start_time_ms += char_duration

    data = {
        "training": training,
        "batch": batch,
        "file_name": file_name,
        "cw_text": cw_text,
        "speed_wpm": speed_wpm,
        "frequency": frequencies,
        "start_time_ms": start_times,
        "duration_ms": duration_ms,
        "file_duration_ms": start_time_ms
    }

    json_file_path = os.path.join(json_directory, file_name.replace(".wav", ".json").replace("cw", "label"))

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


for i in range(num_files_to_generate):
    cw_text = generate_cw_text(random.randint(min_char, max_char))
    wpm = random.randint(speed_range[0], speed_range[1])
    frequency = random.randint(min_frequency, max_frequency)
    generate_json_file(i + 1, cw_text, wpm, frequency)


with open('length.py', 'r') as file:
    code = file.read()
    exec(code)
    
with open('wav_3.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
   # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'json_directory': parametr})
