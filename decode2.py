


def decode_morse_sequence(sequence):

    morse_code_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '-----': '0', '--..--': ',', '.-.-.-': '.', '..--..': '?', '-..-.': '/',
    '-....-': '-', '-.--.': '(', '-.--.-': ')'
    }

    decoded_texts = {}
    current_code = {}
    
    for element, frequency in sequence:
        if frequency not in current_code:
            current_code[frequency] = ""

        if element == 'char_end':
            letter = morse_code_dict.get(current_code[frequency], '')
            decoded_texts[frequency] = decoded_texts.get(frequency, '') + letter
            current_code[frequency] = ""
        else:
            symbol = '.' if element == 'dot' else '-'
            current_code[frequency] += symbol

    # Dodanie ostatnich liter, jeśli sekwencja się zakończyła bez 'char_end'
    for frequency, code in current_code.items():
        if code:  # Sprawdzenie, czy jest jakikolwiek nieprzetworzony kod
            letter = morse_code_dict.get(code, '')
            decoded_texts[frequency] = decoded_texts.get(frequency, '') + letter

    return decoded_texts

# Przykładowe dane wejściowe
sequence = [('dot', 700), ('dash', 700), ('dot', 600), ('dash', 700), ('dot', 600), ('char_end', 700), ('dash', 600), ('char_end', 600), 
            ('dot', 700), ('dash', 700), ('char_end', 700), ('dot', 600), ('dash', 600), ('char_end', 600)]

# Dekodowanie
decoded_texts = decode_morse_sequence(sequence)

# Wyświetlenie wyników
for freq, text in decoded_texts.items():
    print(f"Częstotliwość: {freq}, Tekst: {text}")