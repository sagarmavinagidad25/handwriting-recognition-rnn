const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');
const resultContainer = document.getElementById('resultContainer');
const predictionBadge = document.getElementById('predictionBadge');
const confidenceList = document.getElementById('confidenceList');
const errorText = document.getElementById('errorText');

const thicknessInput = document.getElementById('thickness');
const fileInput = document.getElementById('fileInput');

let isDrawing = false;

// Initialize canvas with black background
function initCanvas() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // Draw with thick white strokes
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = thicknessInput.value;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
}

initCanvas();

thicknessInput.addEventListener('input', (e) => {
    ctx.lineWidth = e.target.value;
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                initCanvas(); // clear first
                // Draw image scaled to fit canvas gracefully
                const ratio = Math.min(canvas.width / img.width, canvas.height / img.height);
                const width = img.width * ratio;
                const height = img.height * ratio;
                const x = (canvas.width - width) / 2;
                const y = (canvas.height - height) / 2;
                ctx.drawImage(img, x, y, width, height);
                // Auto predict
                predictBtn.click();
            }
            img.src = event.target.result;
        }
        reader.readAsDataURL(file);
    }
});

function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

function draw(e) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    
    // Scale coordinates accurately for responsive huge canvas
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    let x, y;
    if (e.type.includes('touch')) {
        e.preventDefault();
        x = (e.touches[0].clientX - rect.left) * scaleX;
        y = (e.touches[0].clientY - rect.top) * scaleY;
    } else {
        x = (e.clientX - rect.left) * scaleX;
        y = (e.clientY - rect.top) * scaleY;
    }

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Event Listeners
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

canvas.addEventListener('touchstart', startDrawing, { passive: false });
canvas.addEventListener('touchmove', draw, { passive: false });
canvas.addEventListener('touchend', stopDrawing);

clearBtn.addEventListener('click', () => {
    initCanvas();
    resultContainer.style.display = 'none';
    errorText.textContent = '';
    fileInput.value = "";
});

function speakText(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Cancel any ongoing speech
        const utterance = new SpeechSynthesisUtterance("Predicted word is: " + text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

predictBtn.addEventListener('click', async () => {
    predictBtn.disabled = true;
    predictBtn.textContent = 'Predicting...';
    errorText.textContent = '';
    resultContainer.style.display = 'none';

    try {
        const dataURL = canvas.toDataURL('image/png');
        
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: dataURL })
        });

        const result = await response.json();

        if (response.ok) {
            predictionBadge.textContent = result.prediction;
            confidenceList.innerHTML = `<p>Confidence: ${(result.confidence * 100).toFixed(2)}%</p>`;
            resultContainer.style.display = 'block';
            
            // Invoke the voice synthesizer
            speakText(result.prediction);
        } else {
            errorText.textContent = `Error: ${result.error || 'Prediction failed'}`;
        }
    } catch (err) {
        console.error(err);
        errorText.textContent = 'Network error: Ensure backend is running.';
    } finally {
        predictBtn.disabled = false;
        predictBtn.textContent = 'Predict Pattern';
    }
});
