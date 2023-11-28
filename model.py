import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Attention
from tensorflow.keras.optimizers import Adam

# Wymiary danych wejściowych - należy je dostosować do Twoich danych
input_shape = (None, num_features)  # 'None' dla zmiennego rozmiaru sekwencji, 'num_features' to liczba cech na krok czasowy

# Parametry modelu - dostosuj je do swoich potrzeb
lstm_units = 128  # Liczba jednostek w warstwach LSTM
dense_units = 64  # Liczba jednostek w warstwach gęsto połączonych
num_classes = 7   # Liczba klas/etykiet do rozpoznania
dropout_rate = 0.5
learning_rate = 0.001


# Parametry wejściowe modelu
input_shape = (None, num_features)  # Dostosuj do swoich danych

# Tworzenie warstwy wejściowej
input_layer = Input(shape=input_shape)

# Dodawanie warstw LSTM
lstm_layer = LSTM(lstm_units, return_sequences=True)(input_layer)
lstm_layer = LSTM(lstm_units, return_sequences=True)(lstm_layer)

# Dodawanie warstwy uwagi
attention_layer = Attention()(lstm_layer)

# Dodawanie warstwy Dropout dla regularyzacji
dropout_layer = Dropout(dropout_rate)(attention_layer)

# Warstwa wspólna
common_dense = Dense(dense_units, activation='relu')(dropout_layer)

# Pierwsza warstwa wyjściowa dla klasyfikacji
classification_output = Dense(num_classes, activation='softmax', name='classification_output')(common_dense)

# Druga warstwa wyjściowa dla frequency i speed_wpm
regression_output = Dense(2, activation='linear', name='regression_output')(common_dense)

# Tworzenie modelu z dwoma wyjściami
model = Model(inputs=input_layer, outputs=[classification_output, regression_output])

# Kompilacja modelu
model.compile(optimizer=Adam(learning_rate=learning_rate),
              loss={'classification_output': 'categorical_crossentropy',
                    'regression_output': 'mean_squared_error'},
              metrics={'classification_output': 'accuracy',
                       'regression_output': ['mae']})

# Wyświetlenie podsumowania modelu
model.summary()
