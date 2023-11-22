MORSE_CODE_DICT = {
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

def decode_morse(json_data):
    message = ''
    current_code = ''

    for element in json_data['data']:
        if element['element'] == 'dot':
            current_code += '.'
        elif element['element'] == 'dash':
            current_code += '-'
        elif element['element'] == 'char_end':
            message += MORSE_CODE_DICT.get(current_code, '')
            current_code = ''
        elif element['element'] == 'word_end':
            message += ' '

    return message.strip()

json_input = {
  "frequency": 758,
  "speed_wpm": 21,
  "output": 1,
  "volume": 0.666,
  "data": [
    {
      "element": "dash",
      "start_ms": 847,
      "duration_ms": 171.42857142857144
    },
    {
      "element": "dot",
      "start_ms": 1075.5714285714287,
      "duration_ms": 57.14285714285711
    },
    {
      "element": "dash",
      "start_ms": 1189.857142857143,
      "duration_ms": 171.42857142857133
    },
    {
      "element": "char_end",
      "start_ms": 1361.2857142857142,
      "duration_ms": 171.42857142857133
    },
    {
      "element": "dash",
      "start_ms": 1532.7142857142856,
      "duration_ms": 171.42857142857133
    },
    {
      "element": "dot",
      "start_ms": 1761.285714285714,
      "duration_ms": 57.14285714285711
    },
    {
      "element": "dash",
      "start_ms": 1875.5714285714282,
      "duration_ms": 171.42857142857133
    },
    {
      "element": "char_end",
      "start_ms": 2046.9999999999995,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "word_end",
      "start_ms": 2218.428571428571,
      "duration_ms": 400.0
    },
    {
      "element": "dash",
      "start_ms": 2618.428571428571,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 2847.0,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dot",
      "start_ms": 2961.2857142857147,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dot",
      "start_ms": 3075.5714285714294,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dot",
      "start_ms": 3189.857142857144,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "char_end",
      "start_ms": 3247.0000000000014,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 3418.428571428573,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dot",
      "start_ms": 3532.7142857142876,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dot",
      "start_ms": 3647.0000000000023,
      "duration_ms": 57.14285714285734
    },
    {
      "element": "dash",
      "start_ms": 3761.285714285717,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 3989.857142857146,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "char_end",
      "start_ms": 4161.285714285717,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 4332.714285714289,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 4447.000000000003,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 4561.2857142857165,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 4675.57142857143,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 4789.857142857144,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 4847.000000000001,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 5018.4285714285725,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 5247.000000000001,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dash",
      "start_ms": 5361.285714285715,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 5589.857142857143,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 5647.0,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "word_end",
      "start_ms": 5818.428571428572,
      "duration_ms": 400.0
    },
    {
      "element": "dash",
      "start_ms": 6218.428571428572,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 6447.0,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 6675.571428571428,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 6789.857142857142,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 6904.142857142856,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 6961.285714285713,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 7132.714285714284,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 7189.857142857141,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dot",
      "start_ms": 7361.285714285713,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 7475.571428571427,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 7589.85714285714,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 7646.999999999997,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 7818.428571428569,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 8046.999999999997,
      "duration_ms": 171.42857142857156
    },
    {
      "element": "dash",
      "start_ms": 8275.571428571426,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "char_end",
      "start_ms": 8446.999999999996,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "word_end",
      "start_ms": 8618.428571428567,
      "duration_ms": 400.0
    },
    {
      "element": "dash",
      "start_ms": 9018.428571428567,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "char_end",
      "start_ms": 9189.857142857138,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dash",
      "start_ms": 9361.285714285708,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dash",
      "start_ms": 9589.857142857136,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 9818.428571428563,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dash",
      "start_ms": 9932.714285714277,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "char_end",
      "start_ms": 10104.142857142848,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 10275.571428571418,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 10389.857142857132,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 10446.999999999989,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dash",
      "start_ms": 10618.42857142856,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 10846.999999999987,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 10904.142857142844,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "word_end",
      "start_ms": 11075.571428571415,
      "duration_ms": 400.0
    },
    {
      "element": "dot",
      "start_ms": 11475.571428571415,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dash",
      "start_ms": 11589.857142857129,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 11818.428571428556,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 11932.71428571427,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "char_end",
      "start_ms": 11989.857142857127,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 12161.285714285697,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 12275.571428571411,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 12389.857142857125,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dot",
      "start_ms": 12504.142857142839,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dash",
      "start_ms": 12618.428571428552,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "char_end",
      "start_ms": 12789.857142857123,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 12961.285714285694,
      "duration_ms": 57.14285714285688
    },
    {
      "element": "dash",
      "start_ms": 13075.571428571408,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dash",
      "start_ms": 13304.142857142835,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dash",
      "start_ms": 13532.714285714263,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "char_end",
      "start_ms": 13704.142857142833,
      "duration_ms": 171.42857142857065
    },
    {
      "element": "dot",
      "start_ms": 13875.571428571404,
      "duration_ms": 57.14285714285688
    }
  ]
}

decoded_message = decode_morse(json_input)
print(decoded_message)
