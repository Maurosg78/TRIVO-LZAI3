
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.optimizers import Adam
import numpy as np

# Configuración básica de la red neuronal
def create_model(vocab_size, embedding_dim, input_length):
    model = Sequential()

    # Capa de Embedding
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=input_length))

    # Capa LSTM para generación secuencial
    model.add(LSTM(128, return_sequences=True))
    model.add(LSTM(128))

    # Capa densa de salida
    model.add(Dense(128, activation='relu'))
    model.add(Dense(vocab_size, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    return model

# Función para entrenar el modelo
def train_model(model, X_train, y_train, batch_size, epochs):
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1)
    return model

# Guardar el modelo
def save_model(model, model_path):
    model.save(model_path)
    print(f"Modelo guardado en {model_path}")

# Cargar el modelo
def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

# Función para generar una receta basada en una semilla de entrada
def generate_recipe(model, seed_sequence, tokenizer, max_sequence_length):
    seed_sequence = tokenizer.texts_to_sequences([seed_sequence])
    seed_sequence = np.array(seed_sequence)

    generated_recipe = model.predict(seed_sequence)
    generated_recipe = tokenizer.sequences_to_texts(generated_recipe)
    return generated_recipe[0]

if __name__ == "__main__":
    # Supón que tienes tu conjunto de datos de entrenamiento y tokenizador aquí
    vocab_size = 5000  # Tamaño del vocabulario, por ejemplo
    embedding_dim = 100
    input_length = 50  # Longitud de la secuencia de entrada

    # Crear el modelo
    model = create_model(vocab_size, embedding_dim, input_length)

    # Suponiendo que tienes X_train e y_train listos, entrenar el modelo
    # train_model(model, X_train, y_train, batch_size=64, epochs=10)

    # Guardar el modelo entrenado
    # save_model(model, 'models/recipe_generation_model/recipe_model.h5')

    # Aquí cargamos un modelo preentrenado
    # model = load_model('models/recipe_generation_model/recipe_model.h5')

    # Para la generación de recetas, usar el modelo con una secuencia de entrada
    # seed = "comenzar con tomate y cebolla"
    # generated_recipe = generate_recipe(model, seed, tokenizer, 50)
    # print("Receta generada:", generated_recipe)

