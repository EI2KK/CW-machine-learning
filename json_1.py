import random
import json

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!.,+"
character_list = list(characters)
speed_range = (12, 35)
min_frequency = 300  
max_frequency = 900  
min_char = 1
max_char = 1

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
    dot_duration_ms = int(60000 / (50 * wpm))
    morse_sequence = morse_code.get(char, '')
    char_duration_ms = 0  
    for symbol in morse_sequence:
        if symbol == '.':
            char_duration_ms += dot_duration_ms
        elif symbol == '-':
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
def generate_json_file(file_number, cw_text):
    file_name = f"label_{file_number:05}.wav"
    speed_wpm = [random.randint(speed_range[0], speed_range[1]) for _ in cw_text]
    frequency = [random.randint(min_frequency, max_frequency) for _ in cw_text]
    duration_ms = [calculate_morse_duration(char, wpm) for char, wpm in zip(cw_text, speed_wpm)]

    total_duration = sum(duration_ms)
    num_chars = len(cw_text)
    
    # Calculate the minimum spacing between characters (e.g., 500 ms)
    min_spacing = 500
    
    # Calculate the maximum available time between characters
    max_available_time = file_duration_ms - total_duration - (num_chars - 1) * min_spacing
    
    # Randomly select an initial start_time_ms
    start_time_ms = random.randint(0, max_available_time)
    
    # Create a list of start_time_ms for each element in cw_text
    start_times = []
    for char, wpm, char_duration in zip(cw_text, speed_wpm, duration_ms):
        start_times.append(start_time_ms)
        start_time_ms += char_duration + min_spacing  # Add the minimum spacing

    data = {
        "file_name": file_name,
        "cw_text": cw_text,
        "speed_wpm": speed_wpm,
        "frequency": frequency,
        "start_time_ms": start_times,
        "duration_ms": duration_ms,
        "file_duration_ms": file_duration_ms
    }

    with open(file_name.replace(".wav", ".json"), "w") as json_file:
        json.dump(data, json_file, indent=4)

num_files_to_generate = 10 

# Generate multiple JSON files with CW (Morse code) data
for i in range(num_files_to_generate):
    cw_text = generate_cw_text(random.randint(min_char, max_char)) 
    generate_json_file(i + 1, cw_text)
