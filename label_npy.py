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

def process_json_files_v7(directory, window, overlap, step_ms):
    element_to_vector = {
        "dot":          "0000001",
        "dash":         "0000010",
        "element_end":  "0000100",
        "char_end":     "0001000",
        "word_end":     "0010000",
        "qrm":          "0100000",
        "pause":        "1000000"
    }

    for filename in os.listdir(directory):
        if filename.startswith("cw_") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)

            sequences = []
            session_duration_ms = data.get("session_duration_ms", 0)

            start_ms = 0
            while start_ms < session_duration_ms:
                end_ms = start_ms + window
                if end_ms > session_duration_ms:
                    end_ms = session_duration_ms

                sequence = {
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "steps": []
                }

                step_start_ms = start_ms
                while step_start_ms < end_ms:
                    step_end_ms = step_start_ms + step_ms
                    step_events = []

                    for element_group in data.get("elements", []):
                        for element in element_group.get("data", []):
                            if (element["end_ms"] < step_end_ms and element["end_ms"] >= step_start_ms):
                                step_events.append({
                                    "frequency": normalize_frequency(element_group["frequency"]),
                                    "speed_wpm": normalize_speed_wpm(element_group["speed_wpm"]),
                                    "element": element_to_vector.get(element["element"], "0000000")
                                })

                    if not step_events:
                        step_events.append({
                            "frequency": 0,
                            "speed_wpm": 0,
                            "element": "0000000"
                        })

                    sequence["steps"].append({
                        "time_ms": step_start_ms,
                        "events": step_events
                    })
                    step_start_ms += step_ms

                sequences.append(sequence)
                start_ms += window - overlap

            label_filename_npy = "label_" + filename.split("_")[1].replace('.json', '.npy')
            label_path_npy = os.path.join(directory, label_filename_npy)
            np.save(label_path_npy, sequences)

step_ms = 23.219954648526078
data_length = 22
overlap = 11

process_json_files_v7(directory, (data_length * step_ms), (overlap * step_ms), step_ms)
