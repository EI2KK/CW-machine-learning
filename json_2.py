import random
import json
import os

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!.,+"
character_list = list(characters)
speed_range = (12, 35)
min_frequency = 300
max_frequency = 900
min_char = 3
max_char = 5
num_files_to_generate = 10
training = 2
batch = 6
noise = False
json_directory_ = 'json_folder'

# Formatowanie wartości z wiodącymi zerami
formatted_training = f"{training:03}"  # Formatuje 'training' do postaci trzycyfrowej
formatted_batch = f"{batch:03}"  # Formatuje 'batch' do postaci trzycyfrowej

json_directory = f"{json_directory_}_{formatted_training}_{formatted_batch}"



## zapis danych o wygenerowanych plikach

json_file_name = 'training.json'

# Formatowanie wartości z wiodącymi zerami
formatted_training = f"{training:03}"  # Formatuje 'training' do postaci trzycyfrowej
formatted_batch = f"{batch:03}"  # Formatuje 'batch' do postaci trzycyfrowej

# Tworzenie nowej nazwy katalogu
json_directory = f"{json_directory_}_{formatted_training}_{formatted_batch}"

# Struktura danych do zapisania
data_to_save = {
    'completed': None,
    'formatted_training': formatted_training,
    'formatted_batch': formatted_batch,
    'json_directory': json_directory,
    'speed_range': speed_range,
    'min_frequency': min_frequency,
    'max_frequency': max_frequency,
    'min_char': min_char,
    'max_char': max_char,
    'num_of_files': num_files_to_generate,
    'noise': noise,
    'tx': False
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
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ',': '--..--',
    '.': '.-.-.-', '+': '.-.-.', '!': '-.-.--', '?': '..--..'
}

# Function to calculate the duration of a Morse code character
def calculate_morse_duration(char, wpm):
    dot_duration_ms = int(1200 / wpm)  # Długość kropki
    dash_duration_ms = 3 * dot_duration_ms  # Długość kreski
    intra_char_space_ms = dot_duration_ms  # Przerwa między elementami znaku

    morse_sequence = morse_code.get(char, '')
    char_duration_ms = 0

    for i, symbol in enumerate(morse_sequence):
        if symbol == '.':
            char_duration_ms += dot_duration_ms
        elif symbol == '-':
            char_duration_ms += dash_duration_ms

        # Dodaj przerwę po każdym symbolu oprócz ostatniego
        if i < len(morse_sequence) - 1:
            char_duration_ms += intra_char_space_ms

    # Dodaj przerwę po znaku (standardowo trzy długości kropki)
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


file_duration_ms = round((max_char * longest_duration) / 2)

# Function to generate a JSON file with CW (Morse code) data
def generate_json_file(file_number, cw_text):
    file_name = f"cw_{file_number:05}.wav"
    speed_wpm = [random.randint(speed_range[0], speed_range[1]) for _ in cw_text]
    frequency = [random.randint(min_frequency, max_frequency) for _ in cw_text]
    duration_ms = [calculate_morse_duration(char, wpm) for char, wpm in zip(cw_text, speed_wpm)]

    total_duration = sum(duration_ms)
    num_chars = len(cw_text)
    
    # Calculate the maximum spacing between characters (e.g., 1000 ms)
    max_spacing = 1000
    
    # Calculate the maximum available time for characters
    max_available_time = file_duration_ms - total_duration
    
    # Randomly select an initial start_time_ms
    start_time_ms = random.randint(0, max_available_time)
    
    # Create a list of start_time_ms for each element in cw_text
    start_times = []
    for char, wpm, char_duration in zip(cw_text, speed_wpm, duration_ms):
        start_times.append(start_time_ms)
        start_time_ms += random.randint(0, max_spacing)  # Randomly choose spacing

    data = {
        "file_name": file_name,
        "cw_text": cw_text,
        "speed_wpm": speed_wpm,
        "frequency": frequency,
        "start_time_ms": start_times,
        "duration_ms": duration_ms,
        "file_duration_ms": file_duration_ms
    }

    
    json_file_path = os.path.join(json_directory, file_name.replace(".wav", ".json").replace("cw", "label"))

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Generate multiple JSON files with CW (Morse code) data
for i in range(num_files_to_generate):
    cw_text = generate_cw_text(random.randint(min_char, max_char))
    generate_json_file(i + 1, cw_text)


with open('length.py', 'r') as file:
    code = file.read()
#    exec(code)
    
    
with open('length.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
   # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'json_directory': parametr})
    


with open('wav_3.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'json_directory': parametr})
    

if noise:
    with open('noise_bulk.py', 'r') as file:
        code = file.read()
        # Tworzenie zmiennej, którą chcesz przekazać
        parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
        # Wykonanie kodu z modyfikacją zmiennych globalnych
        exec(code, {'input_folder': parametr})


    
with open('fftg.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'wav_directory': parametr})    