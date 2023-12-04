import os
import json

if __name__ == '__main__':
    # Ścieżka do katalogu z plikami WAV
    directory = 'json_folder_001_014'



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
    fields_to_copy = ["cw_file", "npy_file", "session_duration_ms", "noise", "S/N (dB)", "speed_range",
                      "freq_range", "start_between_ms", "stop_b4_end", "nr_of_freq",
                      "training", "batch"]

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
            
            label_data = {field: data[field] for field in fields_to_copy if field in data}
            
            label_data = {**label_data, **{
                "sequences": [],
                "session_duration_ms": data.get("session_duration_ms", 0),
}}

            # Tworzenie sekwencji
            start_ms = 0
            while start_ms < label_data["session_duration_ms"]:
                end_ms = start_ms + window
                if end_ms > label_data["session_duration_ms"]:
                    end_ms = label_data["session_duration_ms"]

                sequence = {
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "steps": []
                }

                # Tworzenie kroków dla każdej sekwencji
                step_start_ms = start_ms
                while step_start_ms < end_ms:
                    step_end_ms = step_start_ms + step_ms
                    step_events = []

                    # Szukanie elementów pasujących do kroku czasowego
                    for element_group in data.get("elements", []):
                        for element in element_group.get("data", []):
                            # if (element["start_ms"] < step_end_ms and element["end_ms"] > step_start_ms):
                            if (element["end_ms"] < step_end_ms and element["end_ms"] >= step_start_ms):

                                step_events.append({
                                    "frequency": normalize_frequency(element_group["frequency"]),
                                    "speed_wpm": normalize_speed_wpm(element_group["speed_wpm"]),
                                    "element": element_to_vector.get(element["element"], "0000000")
                                })

                    if not step_events:
                        # Dodanie danych zerowych, jeśli nie znaleziono elementów
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

                label_data["sequences"].append(sequence)

                start_ms += window - overlap

            # Zapisywanie zmodyfikowanych danych do nowego pliku JSON
            label_filename = "label_" + filename.split("_")[1]
            label_path = os.path.join(directory, label_filename)
            with open(label_path, 'w') as label_file:
                json.dump(label_data, label_file, indent=4)

def process_json_files_v_old(directory, window, overlap):
    """
    Processes the .json files in the specified directory, creating corresponding label files.
    Adds empty data entries if no elements are present in a time window.

    Args:
    directory (str): The directory containing the .json files.
    window (int): The window length in milliseconds.
    overlap (int): The overlap length in milliseconds.
    """
    fields_to_copy = ["cw_file", "npy_file", "session_duration_ms", "noise", "S/N (dB)", "speed_range",
                      "freq_range", "start_between_ms", "stop_b4_end", "nr_of_freq",
                      "training", "batch"]

    element_to_vector = {
        "dot":          "0000001",
        "dash":         "0000010",
        "element_end":  "0000100",
        "char_end":     "0001000",
        "word_end":     "0010000",
        "qrm":          "0100000",
        "pause":        "1000000"
    }

    # Normalization functions
    def normalize_frequency(freq):
        return (freq - 300) / (1000 - 300)

    def normalize_speed_wpm(speed):
        
        speed = (speed - 12) / (50 - 12)
        if speed < 0:
            speed = 0
    
        return speed

    # Function to format time values
    def format_time(value):
        return float(f"{value:.4f}")

    for filename in os.listdir(directory):
        if filename.startswith("cw_") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)

            label_filename = "label_" + filename.split("_")[1]
            label_path = os.path.join(directory, label_filename)
            print(f"{label_filename}", end='\r')
            label_data = {field: data[field] for field in fields_to_copy if field in data}

            # Calculate sequences
            session_duration = data.get("session_duration_ms", 0)
            label_data["sequences"] = []
            start = 0
            while start + window <= session_duration:
                label_data["sequences"].append({
                    "start_ms": format_time(start),
                    "end_ms": format_time(start + window),
                    "elements": []
                })
                start += window - overlap

            # Process elements for each sequence
            for sequence in label_data["sequences"]:
                
                for element_group in data.get("elements", []):
                    normalized_frequency = normalize_frequency(element_group["frequency"])
                    normalized_speed_wpm = normalize_speed_wpm(element_group["speed_wpm"])

                    for element in element_group["data"]:
                        if (element["start_ms"] < sequence["end_ms"] and 
                            element["end_ms"] > sequence["start_ms"]):
                            vector = element_to_vector.get(element["element"], "0000000")
                            sequence["elements"].append({
                                "start_ms": format_time(element["start_ms"]),
                                "end_ms": format_time(element["end_ms"]),
                                "element": vector,
                                "frequency": normalized_frequency,
                                "speed_wpm": normalized_speed_wpm
                            })

                # Sort elements within each sequence
                sequence["elements"].sort(key=lambda x: (x["start_ms"], x["frequency"]))

                # Add empty data entry if no elements are present in the sequence
                if not sequence["elements"]:
                    sequence["elements"].append({
                        "start_ms": sequence["start_ms"],
                        "end_ms": sequence["end_ms"],
                        "element": "0000000",
                        "frequency": 0.0,
                        "speed_wpm": 0.0
                    })

            # Remove duplicates from each sequence
            for sequence in label_data["sequences"]:
                unique_elements = []
                seen = set()
                for elem in sequence["elements"]:
                    elem_tuple = (elem["start_ms"], elem["end_ms"], elem["element"], 
                                  elem["frequency"], elem["speed_wpm"])
                    if elem_tuple not in seen:
                        seen.add(elem_tuple)
                        unique_elements.append(elem)
                sequence["elements"] = unique_elements

            # Save the label file
            with open(label_path, 'w') as label_file:
                json.dump(label_data, label_file, indent=4)

# Example usage:
step_ms = 23.219954648526078
data_length = 22
overlap = 11

process_json_files_v7(directory, (data_length * step_ms), (overlap * step_ms), step_ms)
# Note: This is a demonstration and the function needs a real directory path to execute.
