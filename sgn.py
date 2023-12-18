import numpy as np

def morse_code_generator_v3():
    DOT = '.'
    DASH = '-'
    INTERFERENCE = '#'  # Representation for interference
    ELEMENT_PAUSE = ''  # Pause between elements of a character
    CHARACTER_PAUSE = ' '  # Pause between characters
    WORD_PAUSE = ' / '  # Pause between words

    UNIT_TIME = 5  # Time per unit in ms
    DOT_THRESHOLD = 80  # Threshold for a dot in ms
    DASH_THRESHOLD = 90  # Threshold for a dash in ms
    INTERFERENCE_THRESHOLD = 300  # Threshold for interference in ms
    CHARACTER_PAUSE_THRESHOLD = 500  # Threshold for a pause between characters in ms

    current_signal = None
    duration = 0

    while True:
        signal = yield
        if signal == current_signal:
            # Continue accumulating time if signal is the same
            duration += UNIT_TIME
        else:
            if current_signal is not None:
                # Determine the Morse code for the previous signal
                if current_signal == 1:  # Signal was high
                    if duration <= DOT_THRESHOLD:
                        yield DOT
                    elif duration >= DASH_THRESHOLD and duration < INTERFERENCE_THRESHOLD:
                        yield DASH
                    elif duration >= INTERFERENCE_THRESHOLD:
                        yield INTERFERENCE
                else:  # Signal was low (pause)
                    if duration <= DASH_THRESHOLD:
                        yield ELEMENT_PAUSE
                    elif duration <= CHARACTER_PAUSE_THRESHOLD:
                        yield CHARACTER_PAUSE
                    else:
                        yield WORD_PAUSE

            # Reset for the new signal
            current_signal = signal
            duration = UNIT_TIME


# Example of using the generator
morse_gen = morse_code_generator_v3()
next(morse_gen)  # Initialize the generator


# Simulate real-time input

data = np.load('json_folder_001_001/label_00008.npy', allow_pickle=True)



for i in range(70):
    morse_output = ""
    for signal in data[:, i]:
        result = morse_gen.send(signal)
        if result:
            morse_output += result
    if morse_output:         
        print(i, morse_output)

"""

# Zakładając, że masz n klas
num_classes = n
generators = [morse_code_generator_v3() for _ in range(num_classes)]

# Inicjalizacja generatorów
for gen in generators:
    next(gen)

# Zakładając, że masz listę list danych, gdzie każda wewnętrzna lista odpowiada danej klasie
data_per_class = [...]

# Przetwarzanie danych dla każdej klasy
results = [[] for _ in range(num_classes)]
for class_idx, data in enumerate(data_per_class):
    for signal in data:
        result = generators[class_idx].send(signal)
        if result:
            results[class_idx].append(result)

# zbieraie elementow i dekodowanie znakow
from queue import Queue

# Tworzenie kolejki do przechowywania elementów Morse'a
elements_queue = Queue()

# Przyjmowanie sygnałów i przetwarzanie ich
for signal in signals:  # 'signals' to lista sygnałów
    result = morse_gen.send(signal)
    if result:
        if result == ' ':
            # Gdy napotkasz przerwę między znakami, zdekoduj i wyczyść kolejkę
            decoded_character = decode_from_queue(elements_queue)
            morse_output += decoded_character
            elements_queue.queue.clear()
        else:
            # Dodaj elementy do kolejki
            elements_queue.put(result)

# Funkcja do dekodowania znaku z elementów w kolejce
def decode_from_queue(queue):
    # Logika dekodowania znaku Morse'a z elementów w kolejce
    # ...
    return decoded_character



            
"""            