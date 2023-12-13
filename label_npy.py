import os
import json
import numpy as np

if __name__ == '__main__':
    directory = 'json_folder_001_014'

print(directory)

def normalize_frequency(freq):
    return (freq - 300) / (1000 - 300)

def normalize_speed_wpm(speed):
    speed = (speed - 12) / (50 - 12)
    if speed < 0:
        speed = 0
    return speed

def format_time(value):
    return float(f"{value:.4f}")

def process_json_files_v7(directory, num_steps, overlap, step_ms):
    element_to_vector = {
        "dot":          "00000001",
        "dash":         "00000010",
        "element_end":  "00000100",
        "char_end":     "00001000",
        "word_end":     "00010000",
        "qrm":          "00100000",
        "pause":        "01000000",
        "pause":        "10000000"
    }

    for filename in os.listdir(directory):
        if filename.startswith("cw_") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)

            sequences = []
            session_duration_ms = data.get("session_duration_ms", 0)

            start_step_index = 0
            while start_step_index * step_ms < session_duration_ms:
                sequence = {
                    "start_ms": start_step_index * step_ms,
                    "steps": []
                }

                for step_index in range(num_steps):
                    current_step_ms = (start_step_index + step_index) * step_ms
                    next_step_ms = current_step_ms + step_ms
                    step_events = []

                    for element_group in data.get("elements", []):
                        for element in element_group.get("data", []):
                            if (element["end_ms"] < next_step_ms and element["end_ms"] >= current_step_ms):
                                step_events.append({
                                    "step_ms": current_step_ms,
                                    "frequency": normalize_frequency(element_group["frequency"]),
                                    "speed_wpm": normalize_speed_wpm(element_group["speed_wpm"]),
                                    "element": element_to_vector.get(element["element"], "10000000")
                                })

                    # Dodanie elementów zerowych jeśli jest mniej niż 5 elementów
                    while len(step_events) < 5:
                        step_events.append({
                            "step_ms": current_step_ms,
                            "frequency": 0,
                            "speed_wpm": 0,
                            "element": "10000000"
                        })

                    sequence["steps"].append({
                        "time_ms": current_step_ms,
                        "events": step_events
                    })
 


                sequences.append(sequence)
                start_step_index += num_steps - overlap

            label_filename_npy = "label_" + filename.split("_")[1].replace('.json', '.npy')
            label_path_npy = os.path.join(directory, label_filename_npy)
            np.save(label_path_npy, sequences)

# The main execution part of the script, with specified num_steps, overlap, and step_ms



step_ms = 10.0 # 23.219954648526078
num_steps = 50
overlap = 25

process_json_files_v7(directory, num_steps, overlap, step_ms)
