import random
import json
import os

characters = "ABC DEFGH IJK LMNO PQRST UVWXY Z0 1234 56789?!.,+ "
character_list = list(characters)
speed_range = (25, 25)
min_frequency = 700  
max_frequency = 700  
min_char = 7
max_char = 9
num_files_to_generate = 100

# Function to generate Morse code text of a given length
def generate_cw_text(length):
    return [random.choice(character_list) for _ in range(length)]

# Morse code mapping dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ',': '--..--',
    '.': '.-.-.-', '+': '.-.-.', '!': '-.-.--', '?': '..--..', ' ': ' '
}

# Function to calculate the duration of a Morse code character
def calculate_morse_duration(char, wpm):
    dot_duration_ms = int(1200 / wpm)  
    dash_duration_ms = 3 * dot_duration_ms  i
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

    start_time_ms = 0
    start_times = []
    for char_duration in duration_ms:
        start_times.append(start_time_ms)
        start_time_ms += char_duration

    data = {
        "file_name": file_name,
        "cw_text": cw_text,
        "speed_wpm": speed_wpm,
        "frequency": frequencies,
        "start_time_ms": start_times,
        "duration_ms": duration_ms,
        "file_duration_ms": start_time_ms
    }

    json_directory = 'json_folder'
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
