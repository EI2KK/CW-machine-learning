import os
import json

# Zdefiniuj katalog i wartość przerwy
directory = 'json_folder_001_004'  # Podmień na swoją ścieżkę do katalogu
pause_threshold = 2000  # Przerwa w milisekundach

# Funkcja do obliczania przerw między słowami
def calculate_pauses(start_times, durations, pause_threshold):
    pauses = []
    
    # Sprawdzenie przerwy przed pierwszym słowem
    if start_times[0] > pause_threshold:
        pause_info = {
            "last_signal": 0,
            "no_signal": start_times[0],
            "pause_treshold": pause_threshold,
            "Tx_allowed": pause_threshold,
            "Tx_not_allowed": start_times[0]
        }
        pauses.append(pause_info)

    # Sprawdzenie przerw między słowami
    for i in range(len(start_times) - 1):
        end_of_current_word = start_times[i] + durations[i]
        start_of_next_word = start_times[i + 1]
        pause_duration = start_of_next_word - end_of_current_word

        if pause_duration > pause_threshold:
            pause_info = {
                "last_signal": end_of_current_word,
                "no_signal": pause_duration,
                "pause_treshold": pause_threshold,
                "Tx_allowed": end_of_current_word + pause_threshold,
                "Tx_not_allowed": start_of_next_word
            }
            pauses.append(pause_info)
    
    return pauses


# Przetwarzanie plików JSON w katalogu
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        json_path = os.path.join(directory, filename)
        with open(json_path, 'r') as file:
            data = json.load(file)

        pauses = calculate_pauses(data['start_time_ms'], data['duration_ms'], pause_threshold)
        data['pauses'] = pauses

        # Zapisz zmodyfikowane dane do pliku JSON
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)
