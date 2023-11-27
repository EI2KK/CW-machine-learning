import json
import os
import wave
import numpy as np

if __name__ == '__main__':
    directory = 'json_folder'



def generate_tone(frequency, duration, volume=1.0, sample_rate=44100):
    # Generowanie tonu (przykładowy kod, szczegóły zależą od Twojej implementacji)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    
    # Kontrola głośności tonu przez mnożenie każdej próbki przez 'volume'
    tone *= volume

    return tone

def process_json_file(json_file):
    """Przetwarza pojedynczy plik JSON i generuje plik WAV."""
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        sample_rate = 44100  # Próbki na sekundę
        max_duration = data['session_duration_ms'] / 1000  # Maksymalny czas trwania sesji w sekundach
        audio_signal = np.zeros(int(sample_rate * max_duration))  # Inicjalizacja sygnału audio

        for element in data['elements']:
            frequency = element['frequency']
            volume = element['volume']
            for item in element['data']:
                if item['element'] in ['dot', 'dash', 'qrm']:
                    
                    start = item['start_ms'] / 1000
                    duration = item['duration_ms'] / 1000
                    
                    tone = generate_tone(frequency, duration)
                    start_idx = int(start * sample_rate)
                    end_idx = start_idx + len(tone)

                    # Ograniczenie długości tonu, jeśli wykracza poza zakres sygnału audio
                    end_idx = min(end_idx, len(audio_signal))
                    tone = tone[:end_idx - start_idx]

                    audio_signal[start_idx:end_idx] += tone

        # Normalizacja sygnału
        audio_signal *= (32767 * volume) / np.max(np.abs(audio_signal))
        audio_signal = audio_signal.astype(np.int16)

        # Zapisanie do pliku WAV
        output_filename = os.path.splitext(json_file)[0] + '.wav'
        with wave.open(output_filename, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_signal.tobytes())
        
    except Exception as e:
        print(f"Błąd podczas przetwarzania pliku {json_file}: {e}")
        

def process_all_json_files(directory):
    """Przetwarza tylko pliki JSON zaczynające się od 'cw' w podanym katalogu."""
    for filename in os.listdir(directory):
        if filename.endswith('.json') and filename.startswith('cw'):
            process_json_file(os.path.join(directory, filename))

            
print(directory)
process_all_json_files(directory)
