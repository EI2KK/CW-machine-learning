import random
import json
import os

# Zdefiniowanie zmiennych

characters = "ETANIMSOUDKRGWHBCFJLPQVXYZ0123456789?!/"

training = 1
batch = 7
n = 4  # pula znakow do wyboru od poczatku listy

character_list = list(characters)
char_range = (2, 5)
speed_range = (18, 25)
freq_range = (500, 900)
min_sep = 50
qrm_sep = 50
sidetone = 700
start_between_ms = (500, 1500)
stop_b4_end = 1000
nr_of_freq = 2
nr_of_qrm_freq = 1
qrm_length = (800, 8000)
qrm_start_between = (300, 2000)
min_volume = 0.3
pause_probablilty = 35
pause_length = 1600
total_length = 10000
noise = False
num_files_to_generate = 10


json_directory_ = 'json_folder'
# Formatowanie wartości z wiodącymi zerami
formatted_training = f"{training:03}"  # Formatuje 'training' do postaci trzycyfrowej
formatted_batch = f"{batch:03}"  # Formatuje 'batch' do postaci trzycyfrowej

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


# Tworzenie nazwy katalogu i katalogu
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

# Funkcja do generowania danych Morse'a dla pojedynczego znaku
def generate_morse_data(char, start_time, speed, max_end_time):
    unit_duration = 1200 / speed  # Czas trwania pojedynczego dot
    data = []
    morse_elements = morse_code[char]
    for index, element in enumerate(morse_elements):
        # Dodanie kropki lub kreski
        next_time = start_time + (unit_duration if element == '.' else 3 * unit_duration)
        if next_time > max_end_time:
            break
        data.append({"element": "dot" if element == '.' else "dash", "start_ms": start_time, "end_ms": next_time, "duration_ms": next_time - start_time})
        start_time = next_time

        # Dodanie przerwy (element_gap) tylko jeśli to nie jest ostatni element znaku
        if index < len(morse_elements) - 1:
            element_gap = start_time + unit_duration
            if element_gap > max_end_time:
                break
            # Dodanie informacji o przerwie jako 'element_end'
            data.append({"element": "element_end", "start_ms": start_time, "end_ms": start_time + unit_duration, "duration_ms": unit_duration})
            start_time = element_gap

    # Dodanie 'char_end' na koniec, nawet jeśli wykracza to poza max_end_time
    data.append({"element": "element_end", "start_ms": start_time, "end_ms": start_time + unit_duration, "duration_ms": unit_duration})

    return data, start_time

# Funkcja do generowania danych Morse'a dla słowa
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
            data.append({"element": "char_end", "start_ms": start_time, "end_ms": char_end_time, "duration_ms": char_end_time - start_time})
                        
            start_time = char_end_time
        else:
            break

    word_end_time = word_start_time + 7 * 1200 / speed
    if word_end_time <= max_end_time:
        data.append({"element": "word_end", "start_ms": word_start_time, "end_ms": word_end_time, "duration_ms": word_end_time - word_start_time})
        
        if (max_end_time - word_start_time) > pause_length:
                x = random.randint(1, 100)
                if x >= pause_probablilty:
                    word_end_time = word_start_time + pause_length
                    data.append({"element": "pause", "start_ms": word_start_time, "end_ms": word_end_time, "duration_ms": pause_length})
        
        
        start_time = word_end_time
    return data, start_time


def generate_frequencies(nr_of_freq, freq_range, min_sep):
    # Generowanie unikalnego zestawu częstotliwości
    possible_frequencies = set(range(freq_range[0], freq_range[1] + 1))
    frequencies = []

    while len(frequencies) < nr_of_freq and possible_frequencies:
        frequency = random.choice(list(possible_frequencies))
        frequencies.append(frequency)

        # Usuwanie częstotliwości zbyt bliskich do wybranej
        for freq in range(frequency - min_sep, frequency + min_sep + 1):
            possible_frequencies.discard(freq)

    return sorted(frequencies)
    
def generate_qrm_frequencies(nr_of_qrm_freq, freq_range, min_sep, frequencies):
    # Generowanie unikalnego zestawu możliwych częstotliwości
    possible_qrm_frequencies = set(range(freq_range[0], freq_range[1] + 1))

    # Usuwanie częstotliwości zbyt bliskich do już wybranych w frequencies
    for freq in frequencies:
        for near_freq in range(freq - min_sep, freq + min_sep + 1):
            possible_qrm_frequencies.discard(near_freq)

    qrm_frequencies = []

    while len(qrm_frequencies) < nr_of_qrm_freq and possible_qrm_frequencies:
        qrm_frequency = random.choice(list(possible_qrm_frequencies))
        qrm_frequencies.append(qrm_frequency)

        # W tym przypadku, nie usuwamy częstotliwości bliskich do qrm_frequency
        # ponieważ zachowujemy odstęp tylko od frequencies

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
        #frequencies.append(frequency)
        
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
                break  # Wyjdź z pętli, jeśli czas startu się nie zmienił
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
        #qrm_data["data"].extend(data)
        
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






print("wav")
with open('wav_dd.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'directory': parametr})

if noise:
    print("Noise")
    with open('noise_bulk.py', 'r') as file:
        code = file.read()
        # Tworzenie zmiennej, którą chcesz przekazać
        parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
        # Wykonanie kodu z modyfikacją zmiennych globalnych
        exec(code, {'input_folder': parametr})
    
print("fftg")    
with open('fftg.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
   # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'wav_directory': parametr})
    
print("labels")
with open('labels.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'directory': parametr})