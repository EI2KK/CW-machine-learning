import os
import json
import math

json_directory = 'json_folder'  # Change to the correct path to the JSON files directory

def calculate_max_file_duration(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    if not all(key in data for key in ["start_time_ms", "duration_ms"]):
        print(f"File {json_file_path} does not contain the required data.")
        return 0

    last_start_time = data["start_time_ms"][-1]
    last_duration = data["duration_ms"][-1]
    return last_start_time + last_duration + 50

def update_json_file_duration(json_file_path, new_duration):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    data["file_duration_ms"] = new_duration

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Finding the maximum file duration
max_duration = 0
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        json_path = os.path.join(json_directory, filename)
        duration = calculate_max_file_duration(json_path)
        if duration > max_duration:
            max_duration = duration

# Rounding up to the nearest 100 ms
max_duration = math.ceil(max_duration / 100.0) * 100

# Updating all JSON files to the maximum duration
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        json_path = os.path.join(json_directory, filename)
        update_json_file_duration(json_path, max_duration)
        
        
print(f"File {json_path} updated. New value for file_duration_ms: {max_duration}")
