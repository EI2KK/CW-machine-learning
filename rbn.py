"""
import telnetlib
import time

host = "telnet.reversebeacon.net"
port = 7000
call_sign = "EI2KK"  # your callsign here  

try:
    tn = telnetlib.Telnet(host, port)
    print(f"Connected to {host} on port {port}")

    while True:
        data = tn.read_very_eager().decode('ascii')
        if data:
            if "Please enter your call:" in data:
                break
            print(data)
        time.sleep(0.1)

    tn.write((call_sign + "\n").encode('ascii'))

    # Additional filtering after sending the callsign
    time.sleep(1)
    data = tn.read_very_eager().decode('utf-8', errors='ignore')
    lines = data.split('\n')
    for line in lines:
        if call_sign in line:
            line = line.replace(call_sign, '*****')  # Replace your callsign with asterisks
        print(line)

    start_time = time.time()
    duration = 30  # duration in seconds

    while time.time() - start_time < duration:
        data = tn.read_very_eager().decode('utf-8', errors='ignore')
        if data:
            lines = data.split('\n')
            for line in lines:
                if line.startswith(call_sign):
                    line = '*****' + line[len(call_sign):]  # Replace your callsign at the start of the line
                print(line)
        else:
            time.sleep(0.5) 
    
    tn.close()
except Exception as e:
    print(f"Connection error: {e}")


"""
import telnetlib
import time
import socket

host = "telnet.reversebeacon.net"
port = 7000
call_sign = "EI2KK"  # your callsign here  
spot_data = []
def check_server(host, port):
    try:
        with socket.create_connection((host, port), timeout=10):
            print(f"Server {host} is up on port {port}.")
            return True
    except socket.error as err:
        print(f"Cannot connect to {host} on port {port}: {err}")
        return False

try:
    if check_server(host, port):
        tn = telnetlib.Telnet(host, port)
        print(f"Connected to {host} on port {port}")

        while True:
            data = tn.read_very_eager().decode('ascii')
            if data:
                print(f"Received before call sign: {data}")
                if "Please enter your call:" in data:
                    break
            time.sleep(0.1)
        
        time.sleep(1)
        tn.write((call_sign + "\n").encode('ascii'))
        print(f"Call sign {call_sign} sent, waiting for response...")

        time.sleep(2)
        data = tn.read_very_eager().decode('ascii')
        print(f"Received after call sign: {data}")

        if not data:
            print("No data received after sending call sign. closing connection...")
            tn.close() 
            

        start_time = time.time()
        duration = 1800  # duration in seconds

        while time.time() - start_time < duration:
            data = tn.read_very_eager().decode('utf-8', errors='ignore')
            if data:
                print(data)
                if len(data) > 50:
                    spot_data.append(data)
            else:
                time.sleep(0.5)
        
        tn.close()
except Exception as e:
    print(f"Connection error: {e}")

    
bands = {
    "LF/MF": [],
    "160m": [],
    "80m": [],
    "60m": [],
    "40m": [],
    "30m": [],
    "20m": [],
    "17m": [],
    "15m": [],
    "12m": [],
    "10m": [],
    "6m": [],
    "2m": [],
    "70cm": [],
    "other": []
}

def frequency_to_band(frequency):
    frequency = int(frequency)
    band = ""
    
    if frequency == 0:
        band = "LF/MF"
    elif frequency == 1:
        band = "160m"
    elif frequency == 3:
        band = "80m"
    elif frequency == 5:
        band = "60m"
    elif frequency == 7:
        band = "40m"
    elif frequency == 10:
        band = "30m"
    elif frequency == 14:
        band = "20m"
    elif frequency == 18:
        band = "17m"
    elif frequency == 21:
        band = "15m"
    elif frequency == 24:
        band = "12m"
    elif frequency == 28 or frequency == 29:
        band = "10m"
    elif frequency >= 50 and frequency <= 54:
        band = "6m"
    elif frequency >= 144 and frequency <= 146:
        band = "2m"
    else:
        band = "other"
    
    return band  # Przykład

for line in spot_data:
    # Usuń część linii do ":" włącznie
    processed_line = line.split(':', 1)[1]

    # Podziel resztę linii na podstawie spacji
    parts = processed_line.split()

    # Teraz możesz wyciągnąć poszczególne elementy
    frequency_str = parts[0]
    frequency_khz = float(frequency_str) / 1000
    band = frequency_to_band(frequency_khz)
    formatted_frequency_khz = "{:.4f}".format(frequency_khz)
    target = parts[1]
    mode = parts[2]
    signal_level = parts[3] + " " + parts[4]  # np. "18 dB"
    time_utc_str = parts[-1][:-1]  # Usuwa "Z" z końca stringu
    time_utc = time_utc_str[:2] + ":" + time_utc_str[2:]

    # Usuwanie duplikatów
    existing_entry = next((item for item in bands[band] if item['target'] == target), None)
    if existing_entry:
        bands[band].remove(existing_entry)

    bands[band].append({
        'frequency': formatted_frequency_khz,
        'target': target,
        'mode': mode,
        'signal_level': signal_level,
        'time_utc': time_utc
    })

# Przykład wydruku
for band, spots in bands.items():
    print(f"Band {band}:")
    for spot in spots:
        print(spot)
        
with open('spots.txt', 'w') as file:
    for band, spots in bands.items():
        file.write(f"Band {band}:\n")
        for spot in spots:
            file.write(str(spot) + "\n")


"""
DX de LZ5DI-#:   24897.0  RA5R           CW    18 dB  26 WPM  CQ      0923Z
DX de HG0Y-#:    14003.9  EA1EYL         CW    27 dB  20 WPM  CQ      0933Z
DX de JH7CSU1-#:   3507.0  JA1QE          CW    28 dB  24 WPM  CQ      0928Z
"""