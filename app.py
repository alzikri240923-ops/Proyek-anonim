from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Menyimpan pesan sementara di memory
messages = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confess Anonim</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 500px;
            padding: 30px;
        }
        h1 {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 8px;
        }
        p.subtitle {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 25px;
        }
        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            resize: none;
            font-size: 15px;
            outline: none;
            transition: border-color 0.3s;
        }
        textarea:focus {
            border-color: #667eea;
        }
        button {
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
            transition: background 0.3s;
        }
        button:hover {
            background: #5a67d8;
        }
        .messages-section {
            margin-top: 35px;
            border-top: 2px dashed #e2e8f0;
            padding-top: 20px;
        }
        .messages-section h2 {
            font-size: 18px;
            color: #4a5568;
            margin-bottom: 15px;
        }
        .message-card {
            background: #f7fafc;
            border-left: 4px solid #667eea;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 14px;
            color: #2d3748;
            word-wrap: break-word;
        }
        .empty-msg {
            text-align: center;
            color: #a0aec0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤫 Kirim Confess Anonim</h1>
        <p class="subtitle">Kirim pesan secara rahasia tanpa ketahuan siapapun!</p>
        
        <form action="/send" method="POST">
            <textarea name="message" placeholder="Tulis ungkapan atau pesan rahasiamu di sini..." required></textarea>
            <button type="submit">Kirim Pesan Anonim 🚀</button>
        </form>

        <div class="messages-section">
            <h2>Pesan yang Masuk:</h2>
            {% if messages %}
                {% for msg in messages %}
                    <div class="message-card">{{ msg }}</div>
                {% endfor %}
            {% else %}
                <p class="empty-msg">Belum ada pesan yang masuk.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, messages=messages)

@app.route('/send', methods=['POST'])
def send():
    msg = request.form.get('message')
    if msg:
        messages.insert(0, msg)  # Pesan terbaru di paling atas
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

