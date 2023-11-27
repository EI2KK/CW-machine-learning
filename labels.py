import os
import json

if __name__ == '__main__':
    # Ścieżka do katalogu z plikami WAV
    directory = 'json_folder_001_004'

def process_json_files_v7(directory, window, overlap):
    """
    Processes the .json files in the specified directory, creating corresponding label files.
    Adds empty data entries if no elements are present in a time window.

    Args:
    directory (str): The directory containing the .json files.
    window (int): The window length in milliseconds.
    overlap (int): The overlap length in milliseconds.
    """
    fields_to_copy = ["cw_file", "npy_file", "session_duration_ms", "noise", "speed_range",
                      "freq_range", "start_between_ms", "stop_b4_end", "nr_of_freq",
                      "training", "batch"]

    element_to_vector = {
        "dot":          "000001",
        "dash":         "000010",
        "element_end":  "000100",
        "char_end":     "001000",
        "word_end":     "010000",
        "qrm":          "100000",
        
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
                        "element": "000000",
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
# process_json_files_v7("path/to/directory", 1000, 500)
# Note: This is a demonstration and the function needs a real directory path to execute.



# Example usage:
process_json_files_v7(directory, 500, 250)
# Note: This is a demonstration and the function needs a real directory path to execute.
