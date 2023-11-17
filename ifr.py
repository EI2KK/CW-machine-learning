import json
import random
import os

duration_range = (500, 700)
frequency_deviation = 10
directory_path = 'json_folder_001_003'



def add_interference(file_path, readability_threshold=0.1):
    # Odczytanie zawartości pliku JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Generowanie danych o zakłóceniach
    interference_data = {
        'readability_threshold': readability_threshold,
        'interference': [],
        'start_time': [],
        'duration_ms': [],
        'frequency': []
    }


    # Ostatni czas zakończenia zakłóceń
    last_interference_end = 0
    file_duration = data['file_duration_ms']

    for i, start_time in enumerate(data['start_time_ms']):
        duration = data['duration_ms'][i]
        freq = data['frequency'][i]

        # Minimalny czas, przez który znak musi być czytelny
        min_readable_time = start_time + duration * readability_threshold

        # Sprawdzenie, czy istnieje wystarczająco dużo miejsca dla zakłóceń
        if last_interference_end < min_readable_time:
            interference_start = random.randint(last_interference_end, int(min_readable_time))
            # Uwzględnienie maksymalnej długości pliku
            max_interference_duration = file_duration - interference_start
            interference_duration = min(random.randint(*duration_range), max_interference_duration)

            if interference_duration <= 0:
                # Jeśli nie ma miejsca na zakłócenie, pomiń to zakłócenie
                continue

            interference_end = interference_start + interference_duration
            interference_frequency = freq + random.randint(-frequency_deviation, frequency_deviation)

            # Dodanie danych o zakłóceniach
            interference_data['interference'].append('*')
            interference_data['start_time'].append(interference_start)
            interference_data['duration_ms'].append(interference_duration)
            interference_data['frequency'].append(interference_frequency)

            last_interference_end = interference_end
        else:
            # Przypadek, gdy nie ma miejsca na zakłócenia przed min_readable_time
            continue

    # Dodanie danych o zakłóceniach do głównej struktury JSON
    data['interference'] = interference_data

    # Zapisanie zmodyfikowanego pliku JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



# Dla wszystkich plików w katalogu:

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        add_interference(os.path.join(directory_path, filename))

# Powyższy kod należy uruchomić w odpowiednim środowisku z dostępem do plików JSON.
