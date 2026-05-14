# 🧠 AI Handwriting Word Recognition (CNN + LSTM)

This project features an AI-powered handwriting recognition system capable of accurately predicting entire **words** composed of handwritten alphabets (A-Z). It uses a hybrid **CNN + LSTM (RNN) model** trained on the EMNIST dataset, wrapped in a fast Flask backend with a responsive, modern glassmorphism frontend dashboard.

## ✨ Advanced Features Included:
- **Full Word Scanning:** Slices wide canvas drawings horizontally to predict entire words automatically using auto-cropping bounding boxes!
- **Voice Announcer:** Automatically speaks the predicted word aloud using the browser's native text-to-speech engine.
- **Laptop-Sized Canvas:** Huge 800x400 responsive drawing area for writing smoothly.
- **Marker Control:** Dynamically drag a slider to change your marker ink thickness instantly.
- **File Upload:** Upload any image file of handwriting on your PC straight to the canvas and predict it.

---

## 🛠️ Folder Structure
```
handwriting-rnn-project/
├── model/
│   ├── train.py       # Trains the CNN+LSTM model on EMNIST data
│   ├── predict.py     # Image cropping, segmentation, and inference logic
│   ├── model.h5       # Brain Checkpoint (generated after training)
├── backend/
│   ├── app.py         # Flask Web Server API & static router
├── frontend/
│   ├── index.html     # Web dashboard UI
│   ├── style.css      # Modern Glassmorphism Styling
│   ├── script.js      # Canvas drawing & voice execution logic
├── requirements.txt   # Python Dependencies
└── README.md          # Project Instructions (This guide)
```

---

## 🚀 How to Run the Project (Step-by-Step Guide)

Whenever you open this project in Visual Studio Code, follow these exact steps to run it:

### **Step 1: Open Your Terminal**
Open a new Terminal in VS Code (`Terminal -> New Terminal`). Ensure you are in the project folder:
```powershell
cd C:\Users\SAGAR\Desktop\ml2\handwriting-rnn-project
```

### **Step 2: Activate the Virtual Environment**
Activate your Python isolated brain environment to load all installed ML dependencies:
```powershell
.\venv\Scripts\activate
```
*(You should see `(venv)` appear on the left side of your terminal line).*

### **Step 3 (Optional): Retrain the AI**
*(You only need to do this if you want to make the model smarter or train it from scratch)*
Run the training engine. It will download the EMNIST datasets, iterate through 3 fast epochs, and securely save the 90%+ accurate graph to `model.h5`:
```powershell

```
*(Wait ~50 seconds until it says "Model Saved")*

### **Step 4: Start the Backend Server**
Start the AI Flask engine to serve the UI and process drawing logic:
```powershell
python backend/app.py
```
*(Keep this terminal open and running!)*

### **Step 5: Open the Web Application**
Now that the backend is active, open your favorite web browser (Chrome/Edge/Safari) and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### **Step 6: Predict!**
1. Draw a word with your mouse on the black canvas. **(Make sure you leave a small physical gap between each letter so the script can slice them properly!)**
2. Hit **"Predict Pattern"**.
3. Listen to the Voice Announcer tell you what you drew and view your individual confidence percentages!
python model/train.py