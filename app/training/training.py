import tensorflow as tf

class TrainingController:
    def __init__(self):
        self.model = tf.keras.models.Sequential()

    def load_data(self, data_path):
        self.training_data = tf.keras.preprocessing.text_dataset_from_directory(
            data_path, batch_size=32, validation_split=0.2, subset="training", seed=42
        )
        self.validation_data = tf.keras.preprocessing.text_dataset_from_directory(
            data_path, batch_size=32, validation_split=0.2, subset="validation", seed=42
        )
        return self.training_data, self.validation_data

    def preprocess_data(self, data):
        preprocessed_data = data.map(lambda x, y: (tf.expand_dims(x, -1), y))
        return preprocessed_data

    def train(self, training_data, validation_data, epochs=10, batch_size=32, learning_rate=0.001):
        print("Training the model...")
        self.model.add(tf.keras.layers.Embedding(10000, 16, input_length=1))
        self.model.add(tf.keras.layers.GlobalAveragePooling1D())
        self.model.add(tf.keras.layers.Dense(16, activation="relu"))
        self.model.add(tf.keras.layers.Dense(1, activation="sigmoid"))
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )
        self.model.fit(training_data, validation_data, epochs=epochs, batch_size=batch_size, validation_data=validation_data)
        print("Model training completed.")

    def evaluate(self, test_data):
        print("Evaluating the model...")
        test_loss, test_accuracy = self.model.evaluate(test_data)
        print(f"Test loss: {test_loss}, Test accuracy: {test_accuracy}")
        return test_loss, test_accuracy

    def save_model(self, model_path):
        print("Saving the model...")
        self.model.save(model_path)
        print(f"Model saved to {model_path}")

    def load_model(self, model_path):
        print("Loading the model...")
        self.model = tf.keras.models.load_model(model_path)
        print(f"Model loaded from {model_path}")
