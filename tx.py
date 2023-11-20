import os
import json

# Zdefiniuj katalog i wartość przerwy
directory = 'json_folder_002_004'  # Podmień na swoją ścieżkę do katalogu
pause_threshold = 2000  # Przerwa w milisekundach

# Funkcja do obliczania przerw między słowami
def calculate_pauses(start_times, durations, pause_threshold):
    pauses = []
    for i in range(len(start_times) - 1):
        end_of_current_word = start_times[i] + durations[i]
        start_of_next_word = start_times[i + 1]
        pause_duration = start_of_next_word - end_of_current_word
        print(pause_duration)
        if pause_duration > pause_threshold:
            pauses.append(pause_duration)
    return pauses

# Przetwarzanie plików JSON w katalogu
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        json_path = os.path.join(directory, filename)
        with open(json_path, 'r') as file:
            data = json.load(file)

        pauses = calculate_pauses(data['start_time_ms'], data['duration_ms'], pause_threshold)
        #print(pauses)
        # Dodaj informacje o przerwach do danych JSON, jeśli są jakieś dłuższe przerwy
        data['pauses'] = pauses

        # Zapisz zmodyfikowane dane do pliku JSON
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)
