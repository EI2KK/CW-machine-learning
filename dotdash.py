import random
import json
import os

# Zdefiniowanie zmiennych
characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?! "
character_list = list(characters)
char_range = (2, 7)
speed_range = (18, 25)
freq_range = (500, 900)
min_sep = 50
sidetone = 700
start_between_ms = (500, 1500)
stop_b4_end = 1000
nr_of_freq = 4
min_volume = 0.3
total_length = 10000
noise = True
num_files_to_generate = 10
training = 1
batch = 4
json_directory_ = 'json_folder'
# Formatowanie wartości z wiodącymi zerami
formatted_training = f"{training:03}"  # Formatuje 'training' do postaci trzycyfrowej
formatted_batch = f"{batch:03}"  # Formatuje 'batch' do postaci trzycyfrowej


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
        next_time = start_time + (unit_duration if element == '.' else 3 * unit_duration)
        if next_time > max_end_time:
            break
        data.append({"element": "dot" if element == '.' else "dash", "start_ms": start_time, "duration_ms": next_time - start_time})
        start_time = next_time

        # Dodanie przerwy tylko jeśli to nie jest ostatni element znaku
        if index < len(morse_elements) - 1:
            element_gap = start_time + unit_duration
            if element_gap > max_end_time:
                break
            start_time = element_gap

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
        if char_end_time <= max_end_time:
            data.append({"element": "char_end", "start_ms": start_time, "duration_ms": char_end_time - start_time})
            start_time = char_end_time
        else:
            break

    word_end_time = start_time + 7 * 1200 / speed
    if word_end_time <= max_end_time:
        data.append({"element": "word_end", "start_ms": start_time, "duration_ms": word_end_time - start_time})
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

for file_number in range(1, num_files_to_generate + 1):

    json_data = {
        "cw_file": f"cw_{file_number:05}.wav",
        "session_duration_ms": total_length, 
        "noise": noise,
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
    for _ in range(nr_of_freq):
    
        frequency = frequencies[_]
        #frequencies.append(frequency)
        
        speed = random.randint(*speed_range)
        start_time = random.randint(*start_between_ms)
        volume = round(random.uniform(min_volume, 1), 3)
        freq_data = {"frequency": frequency, "speed_wpm": speed, "output": 0, "volume": volume, "data": []}  # Dodano 'volume'


        while start_time < total_length - stop_b4_end:
            word_length = random.randint(*char_range)
            word = ''.join(random.choices(character_list, k=word_length))
            word_data, new_start_time = generate_word_data(word, start_time, speed, total_length - stop_b4_end)
            if new_start_time == start_time:
                break  # Wyjdź z pętli, jeśli czas startu się nie zmienił
            start_time = new_start_time
            freq_data["data"].extend(word_data)

        json_data["elements"].append(freq_data)

    closest_freq = min(frequencies, key=lambda x: (abs(x - sidetone), -x))
    for element in json_data["elements"]:
        if element["frequency"] == closest_freq:
            element["output"] = 1

    file_name = f"cw_{file_number:05}.json"
    file_path = os.path.join(directory_name, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)




if noise:
    with open('noise_bulk.py', 'r') as file:
        code = file.read()
        # Tworzenie zmiennej, którą chcesz przekazać
        parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
        # Wykonanie kodu z modyfikacją zmiennych globalnych
        exec(code, {'input_folder': parametr})



with open('wav_dd.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
    # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'directory': parametr})
    
with open('fftg.py', 'r') as file:
    code = file.read()
    # Tworzenie zmiennej, którą chcesz przekazać
    parametr = f"{json_directory_}_{formatted_training}_{formatted_batch}"
   # Wykonanie kodu z modyfikacją zmiennych globalnych
    exec(code, {'wav_directory': parametr})