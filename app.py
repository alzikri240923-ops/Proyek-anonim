from flask import Flask, request, render_template_string

app = Flask(__name__)

SOLUTION = [
    ['T', 'O', 'P', 'I', '#'],
    ['A', '#', 'A', '#', '#'],
    ['K', 'I', 'T', 'A', '#'],
    ['U', '#', 'U', '#', '#'],
    ['#', '#', 'K', 'A', 'U']
]

NUMBERS = [
    [1,   None, 2,   None, None],
    [None,None, None,None, None],
    [3,   None, None,None, None],
    [None,None, None,None, None],
    [None,None, 4,   None, None]
]

ACROSS_CLUES = [
    {"num": 1, "clue": "Penutup kepala (4 huruf)", "row": 0, "col": 0, "len": 4},
    {"num": 3, "clue": "Saya dan kamu (4 huruf)", "row": 2, "col": 0, "len": 4},
    {"num": 4, "clue": "Kata ganti orang kedua / Kamu (3 huruf)", "row": 4, "col": 2, "len": 3}
]

DOWN_CLUES = [
    {"num": 1, "clue": "Perasaan takut / tidak berani (4 huruf)", "row": 0, "col": 0, "len": 4},
    {"num": 2, "clue": "Mematuk / paruh burung (5 huruf)", "row": 0, "col": 2, "len": 5}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teka-Teki Silang (TTS)</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #f0f2f5; margin: 0; padding: 15px; display: flex; justify-content: center; }
        .container { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
        h2 { text-align: center; color: #1a73e8; margin-top: 0; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #5f6368; font-size: 14px; margin-bottom: 15px; }
        
        .score-board { text-align: center; font-size: 16px; font-weight: bold; margin-bottom: 15px; background: #e8f0fe; padding: 10px; border-radius: 8px; color: #1967d2; }
        
        .crossword-board {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 4px;
            width: 100%;
            max-width: 320px;
            margin: 0 auto 20px auto;
            aspect-ratio: 1 / 1;
        }
        .cell-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
        }
        .cell-number {
            position: absolute;
            top: 2px;
            left: 4px;
            font-size: 10px;
            font-weight: bold;
            color: #3c4043;
            z-index: 2;
            pointer-events: none;
        }
        .cell-input {
            width: 100%;
            height: 100%;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            text-transform: uppercase;
            border: 2px solid #3c4043;
            border-radius: 4px;
            outline: none;
            background: #ffffff;
            color: #202124;
        }
        .cell-input:focus { border-color: #1a73e8; background: #e8f0fe; }
        .cell-black {
            background-color: #202124;
            border: 2px solid #202124;
            border-radius: 4px;
            width: 100%;
            height: 100%;
        }
        
        button { width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #1557b0; }
        
        .clues-container { margin-top: 20px; display: flex; flex-direction: column; gap: 15px; }
        .clue-section h3 { margin: 0 0 8px 0; font-size: 16px; color: #1a73e8; border-bottom: 2px solid #e8f0fe; padding-bottom: 4px; }
        .clue-list { list-style: none; padding: 0; margin: 0; font-size: 14px; color: #3c4043; }
        .clue-list li { margin-bottom: 6px; line-height: 1.4; }

        .message { margin-top: 15px; padding: 10px; border-radius: 6px; text-align: center; font-weight: bold; }
        .success { background: #e6f4ea; color: #137333; border: 1px solid #ceead6; }
        .warning { background: #fef7e0; color: #b06000; border: 1px solid #feefc3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Teka-Teki Silang</h2>
        <div class="subtitle">Isi kotak kosong sesuai petunjuk di bawah!</div>

        {% if score is not none %}
            <div class="score-board">Skor Anda: {{ score }} / {{ total_cells }} Ketepatan ({{ percentage }}%)</div>
        {% endif %}

        <form method="POST">
            <div class="crossword-board">
                {% for r in range(5) %}
                    {% for c in range(5) %}
                        <div class="cell-wrapper">
                            {% if solution[r][c] == '#' %}
                                <div class="cell-black"></div>
                            {% else %}
                                {% if numbers[r][c] %}
                                    <span class="cell-number">{{ numbers[r][c] }}</span>
                                {% endif %}
                                <input type="text" 
                                       name="cell_{{r}}_{{c}}" 
                                       class="cell-input" 
                                       maxlength="1" 
                                       value="{{ user_inputs.get('cell_' ~ r ~ '_' ~ c, '') }}" 
                                       autocomplete="off">
                            {% endif %}
                        </div>
                    {% endfor %}
                {% endfor %}
            </div>

            <button type="submit">Cek Jawaban</button>
        </form>

        {% if message %}
            <div class="message {{ msg_class }}">{{ message }}</div>
        {% endif %}

        <div class="clues-container">
            <div class="clue-section">
                <h3>Mendatar (Across)</h3>
                <ul class="clue-list">
                    {% for item in across_clues %}
                        <li><strong>{{ item.num }}.</strong> {{ item.clue }}</li>
                    {% endfor %}
                </ul>
            </div>
            <div class="clue-section">
                <h3>Menurun (Down)</h3>
                <ul class="clue-list">
                    {% for item in down_clues %}
                        <li><strong>{{ item.num }}.</strong> {{ item.clue }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    user_inputs = {}
    score = None
    percentage = 0
    total_cells = 0
    message = ""
    msg_class = ""

    for r in range(5):
        for c in range(5):
            if SOLUTION[r][c] != '#':
                total_cells += 1

    if request.method == 'POST':
        correct_count = 0
        filled_count = 0

        for r in range(5):
            for c in range(5):
                if SOLUTION[r][c] != '#':
                    key = f"cell_{r}_{c}"
                    val = request.form.get(key, '').strip().upper()
                    user_inputs[key] = val
                    
                    if val:
                        filled_count += 1
                    if val == SOLUTION[r][c]:
                        correct_count += 1

        score = correct_count
        percentage = int((correct_count / total_cells) * 100)

        if correct_count == total_cells:
            message = "Selamat! Semua jawaban Anda benar!"
            msg_class = "success"
        elif filled_count == 0:
            message = "Silakan isi kotak jawaban terlebih dahulu."
            msg_class = "warning"
        else:
            message = f"Anda menjawab {correct_count} dari {total_cells} huruf dengan benar. Coba lagi!"
            msg_class = "warning"

    return render_template_string(
        HTML_TEMPLATE,
        solution=SOLUTION,
        numbers=NUMBERS,
        across_clues=ACROSS_CLUES,
        down_clues=DOWN_CLUES,
        user_inputs=user_inputs,
        score=score,
        percentage=percentage,
        total_cells=total_cells,
        message=message,
        msg_class=msg_class
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
