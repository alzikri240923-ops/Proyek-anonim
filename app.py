from flask import Flask, request, render_template_string

app = Flask(__name__)

riddles = [
    {"question": "Ada di atas kepala, tapi tidak punya rambut, apakah itu?", "answer": "topi"},
    {"question": "Aku selalu ada di depanmu tapi tak bisa dilihat, siapakah aku?", "answer": "masa depan"},
    {"question": "Makin dipotong makin besar, apakah itu?", "answer": "lubang"}
]

current_riddle_idx = 0
score = 0
message = ""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Tebak Teka-Teki</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h2 { color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .message { margin-top: 15px; font-weight: bold; }
        .correct { color: green; }
        .wrong { color: red; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Game Tebak Teka-Teki</h2>
        <p>Skor Anda: {{ score }}</p>
        <p><strong>Pertanyaan:</strong> {{ riddle['question'] }}</p>
        <form method="POST">
            <input type="text" name="answer" placeholder="Jawaban Anda..." required autocomplete="off">
            <button type="submit">Kirim Jawaban</button>
        </form>
        {% if message %}
            <p class="message {{ msg_class }}">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_riddle_idx, score, message
    msg_class = ""
    
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = riddles[current_riddle_idx]['answer'].lower()
        
        if user_answer == correct_answer:
            message = "Benar! Hebat sekali."
            msg_class = "correct"
            score += 1
            current_riddle_idx = (current_riddle_idx + 1) % len(riddles)
        else:
            message = "Jawaban kurang tepat. Coba lagi!"
            msg_class = "wrong"
            
    return render_template_string(HTML_TEMPLATE, 
                                  riddle=riddles[current_riddle_idx], 
                                  score=score, 
                                  message=message, 
                                  msg_class=msg_class)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
