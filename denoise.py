import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten, Reshape, LSTM

# Parametry
input_shape = (22, 33, 1)  # 22 kroki czasowe, 33 cechy, 1 kanał
num_classes = 33           # Liczba cech na wyjściu (taka sama jak na wejściu)

# Budowanie modelu
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

# Dodanie warstwy LSTM
model.add(Reshape((-1, 128)))  # Dopasowanie wymiarów dla LSTM
model.add(LSTM(64, return_sequences=True))

# Dopasowanie wymiarów wyjścia do wejścia
model.add(Dense(num_classes, activation='linear')) 
model.add(Reshape((22, 33)))

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()
