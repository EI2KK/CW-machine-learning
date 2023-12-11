import numpy as np

# Wczytanie pliku .npy
data = np.load('json_folder_001_014/label_00001.npy', allow_pickle=True)

# Wyświetlenie pierwszego elementu
print("Ilosc sekwencji:", len(data))
print("Ilosc krokow: ", len(data[0]["steps"]))
print("=================")
print("=================")
x = len(data) -1
for i in range(x):
    print("Sequence", i, len(data[i]["steps"]), "steps.")

    #print("=================")
    #print(data[i]["steps"][11]["events"])
    #print(data[i+1]["steps"][0]["events"])
    #print("=================")



"""
# Przeglądanie wszystkich elementów
print("\nWszystkie elementy:")
for element in data:
    print(element)

# Wczytanie pliku .npy
data = np.load('json_folder_001_014/cw_00001.npy', allow_pickle=True)

# Wyświetlenie pierwszego elementu
data = data.T
print(data.shape)
print("Pierwszy element: ", len(data), "sets")
print(data[300:310, 0:6])
"""