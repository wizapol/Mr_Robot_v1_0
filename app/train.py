def train_model(chat_controller, training_data):
    chat_controller.training_controller.train(chat_controller.model, training_data)
