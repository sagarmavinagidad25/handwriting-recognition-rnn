import os
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

def load_recognition_model():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.h5')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file model.h5 not found. Please train the model first.")
    
    # We load standard keras model
    return tf.keras.models.load_model(model_path)

def preprocess_image(image_path_or_obj):
    if isinstance(image_path_or_obj, str):
        img = Image.open(image_path_or_obj)
    else:
        # It's a PIL Image object
        img = image_path_or_obj
        
    img = img.convert('L')
    img_arr = np.array(img)
    if np.mean(img_arr) > 127:
        img = ImageOps.invert(img)
        img_arr = np.array(img)

    # 1. Identify non-empty columns to segment words into letters
    non_empty_mask = img_arr > 10
    col_sums = np.sum(non_empty_mask, axis=0) # Count of non-blank pixels per column
    
    is_char = col_sums > 0
    diff = np.diff(is_char.astype(int))
    
    starts = np.where(diff == 1)[0] + 1
    if is_char[0]:
        starts = np.insert(starts, 0, 0)
        
    ends = np.where(diff == -1)[0]
    if is_char[-1]:
        ends = np.append(ends, len(is_char) - 1)
        
    # If canvas is completely empty
    if len(starts) == 0:
        return np.empty((0, 28, 28, 1))

    processed_chars = []
    
    for start, end in zip(starts, ends):
        # A segment is a vertical slice
        # Min width to filter out tiny dust / single-pixel artifacts
        if end - start < 3:
            continue
            
        char_slice = img_arr[:, start:end+1]
        
        # Now vertically crop this specific segment
        char_mask = char_slice > 10
        if not np.any(char_mask):
            continue
            
        y_coords = np.argwhere(char_mask)[:, 0]
        y0, y1 = y_coords.min(), y_coords.max()
        
        cropped = char_slice[y0:y1+1, :]
        
        # Pad to make it a perfect square before resizing
        h, w = cropped.shape
        side = max(h, w)
        pad_y = (side - h) // 2
        pad_x = (side - w) // 2
        
        square = np.pad(cropped, ((pad_y, side - h - pad_y), (pad_x, side - w - pad_x)), mode='constant')
        
        # Add 15% margin to match EMNIST standard sizing
        margin = int(side * 0.15)
        square = np.pad(square, margin, mode='constant')
        
        char_img = Image.fromarray(square)
        char_img = char_img.resize((28, 28), Image.Resampling.LANCZOS)
        char_arr = np.array(char_img).astype('float32') / 255.0
        processed_chars.append(char_arr.reshape(28, 28, 1))
        
    if not processed_chars:
        return np.empty((0, 28, 28, 1))
        
    return np.array(processed_chars)

def predict_character(model, image_path_or_obj):
    processed_batch = preprocess_image(image_path_or_obj)
    
    if processed_batch.shape[0] == 0:
        return "Nothing Drawn", 0.0
        
    predictions = model.predict(processed_batch)
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    word = ""
    confidences = []
    
    for pred in predictions:
        class_idx = np.argmax(pred)
        confidence = float(np.max(pred))
        word += letters[class_idx]
        confidences.append(confidence)
        
    avg_confidence = sum(confidences) / len(confidences)
    
    return word, avg_confidence

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        model = load_recognition_model()
        word, conf = predict_character(model, img_path)
        print(f"Predicted Word: {word} (Avg Confidence: {conf:.2f})")
    else:
        print("Usage: python predict.py <path_to_image>")
