import numpy as np

def podziel_na_porcje(npy_data, num_steps=22, num_features=33):
    # Sprawdzenie, czy dane mają właściwą liczbę cech
    if npy_data.shape[1] != num_features:
        raise ValueError(f"Oczekiwano {num_features} cech, otrzymano {npy_data.shape[1]}")

    # Inicjalizacja listy na paczki danych
    paczki = []

    # Podział danych na paczki
    for i in range(0, npy_data.shape[0] - num_steps + 1, num_steps):
        paczka = npy_data[i:i + num_steps, :]
        paczki.append(paczka)

    return np.array(paczki)

# Ścieżka do pliku .npy
npy_path = 'json_folder_001_014/cw_00001.npy'

# Wczytanie danych
npy_data = np.load(npy_path)

# Podział danych na paczki
paczki_danych = podziel_na_porcje(npy_data)

print("Liczba paczek:", paczki_danych.shape[0])
print("Wymiary paczki:", paczki_danych.shape[1:])
