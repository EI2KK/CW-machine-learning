import random
import json
import os

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!?"
character_list = list(characters)
speed_range = (12, 20)
min_frequency = 600  
max_frequency = 800  
min_word = 1
max_word = 5  # Maksymalna liczba słów w jednym pliku
min_char = 2
max_char = 7  # Maksymalna liczba znaków w jednym słowie
num_files_to_generate = 100
start_between = (300, 2200)
training = 2
batch = 4
json_directory_ = 'json_folder'
noise = False


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
    'min_word': min_word,
    'max_word': max_word,
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


    

# Funkcja do generowania losowego słowa
def generate_word():
    word_length = random.randint(min_char, max_char)
    return ''.join([random.choice(character_list) for _ in range(word_length)])

# Funkcja do generowania Morse code text
def generate_cw_text():
    num_words = random.randint(min_word, max_word)
    return [generate_word() for _ in range(num_words)]
    
    
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
file_duration_ms = ((max_char + 1) * max_word) * longest_duration

# Function to generate a JSON file with CW (Morse code) data
# Funkcja do generowania JSON z danymi CW (kodem Morse'a)
def generate_json_file(file_number, cw_text):

    file_name = f"cw_{file_number:05}.wav"

    # Oblicz przerwę między słowami na podstawie wybranej prędkości
    wpm = random.randint(speed_range[0], speed_range[1])
    dash_duration_ms = calculate_morse_duration('-', wpm)
    word_spacing = dash_duration_ms * 3  # Przerwa między słowami (3 kreski)

    num_words = len(cw_text)  # Poprawione: użyj liczby słów w tekście

    # Oblicz total_duration jako suma długości trwania słów
    total_duration = sum([sum([calculate_morse_duration(char, wpm) for char in word]) for word in cw_text])


    # Oblicz maksymalny dostępny czas między słowami
    max_available_time = file_duration_ms - total_duration - (num_words) * word_spacing

    # Sprawdź, czy max_available_time jest większe lub równe zeru
    if max_available_time >= 0:
        # Losowo wybierz początkowy start_time_ms
        start_time_ms = random.randint(*start_between) # max_available_time)
    else:
        # Jeśli max_available_time jest ujemne, ustaw start_time_ms na zero
        start_time_ms = 0

    # Utwórz listę start_time_ms dla każdego słowa w cw_text
    start_times = []
    duration_ms = []  # Lista przechowująca długość trwania każdego słowa

    for word in cw_text:
        start_times.append(start_time_ms)
        word_duration = sum([calculate_morse_duration(char, wpm) for char in word])
        duration_ms.append(word_duration)  # Dodaj długość trwania słowa
        start_time_ms += word_duration + word_spacing + round(random.uniform(0, 2500))  # Dodaj przerwę między słowami

    # Przemieszczamy speed_wpm i frequency przed file_duration
    speed_wpm = random.randint(speed_range[0], speed_range[1])
    frequency = random.randint(min_frequency, max_frequency)


    # Obliczanie wartości 'eot'
    eot = start_times[-1] + duration_ms[-1] + int(word_spacing * random.uniform(1.6, 2.5))
    
    
    data = {
        "training": training,
        "batch": batch,
        "file_name": file_name,
        "cw_text": cw_text,
        "start_time_ms": start_times,
        "duration_ms": duration_ms,  # Zmienione na listę długości trwania słów
        "speed_wpm": speed_wpm,  # Przeniesione na poziom pliku, jako pojedyncza wartość
        "frequency": frequency,  # Przeniesione na poziom pliku, jako pojedyncza wartość
        "eot": eot,
        "file_duration_ms": file_duration_ms
    }

    # Zapisz dane do pliku JSON
    #json_directory = 'json_folder'
    
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)
    
    json_file_path = os.path.join(json_directory, file_name.replace(".wav", ".json").replace("cw", "label"))

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)




# Generate multiple JSON files with CW (Morse code) data
for i in range(num_files_to_generate):
    cw_text = generate_cw_text()
    generate_json_file(i + 1, cw_text)


with open('length.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
   # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'json_directory': parametr})
    


with open('wav_w.py', 'r') as file:
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
        exec(code, {'json_directory': parametr})

    
    
with open('fftg.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'wav_directory': parametr})