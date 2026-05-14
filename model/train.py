import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Reshape, Conv2D, MaxPooling2D, Flatten, TimeDistributed
from emnist import extract_training_samples, extract_test_samples
import matplotlib.pyplot as plt

# Using EMNIST Letters dataset
print("Loading EMNIST letters dataset...")
# EMNIST letters has 26 classes (1-26), we'll shift them to 0-25
X_train, y_train = extract_training_samples('letters')
X_test, y_test = extract_test_samples('letters')

y_train = y_train - 1
y_test = y_test - 1

# Preprocessing: The 'emnist' python package already handles the 
# transposition needed for EMNIST to be upright, so no rotation/flipping needed.
def preprocess_images(images):
    # EMNIST images are 28x28
    # Just normalize
    processed = np.array(images, dtype='float32') / 255.0
    return processed

print("Preprocessing images...")
X_train = preprocess_images(X_train)
X_test = preprocess_images(X_test)

# To use CNN + LSTM
# Reshape for CNN: (batch, 28, 28, 1)
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

print("Building CNN + LSTM model...")
model = Sequential([
    # CNN for feature extraction
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # Reshape for LSTM: treat height/width/channels as sequence and features
    # After 2 MaxPoolings, size is 5x5x64. Let's reshape to (sequence_length=5, features=5*64=320)
    Reshape((5, 320)),
    
    # RNN (LSTM)
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    
    # Output (26 letters)
    Dense(26, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Training settings
EPOCHS = 3 # As requested: train only 3 epochs
BATCH_SIZE = 128

print(f"Training for {EPOCHS} epochs...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE
)

# Save model
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.h5')
# Saved in .h5 format for compatibility
model.save(model_path)
print(f"Model saved to {model_path}")

# Optional: plot metrics
plt.figure()
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accuracy.png'))
