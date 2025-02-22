from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Хранилище голосов
votes = {"good": 0, "bad": 0}

# Меню по дням недели
weekly_menu = {
    0: "Понедельник: Каша рисовая, кофейный напиток, бутерброд",
    1: "Вторник: Каша геркулес, чай, фрукты",
    2: "Среда: Каша манная, чай, бутерброд",
    3: "Четверг: Каша гречневая, чай, фрукты",
    4: "Пятница: Каша рисовая, какао, бутерброд",
    5: "Суббота: 1, 2, 3",
    6: "Воскресенье: 3, 2, 1"
}

# HTML-шаблон вашего сайта
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Мониторинг питания</title>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">  
  <style>
    body {
      font-family: 'Arial', sans-serif;
      background-color: #f8f9fa;
      margin: 0;
      padding: 0;
    }

    .container {
      max-width: 600px;
      margin: 50px auto;
      padding: 20px;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h1 {
      font-size: 36px;
      margin-bottom: 20px;
      color: #343a40;
      text-align: center;
    }

    .menu, .rating, .votes {
      font-size: 20px;
      margin-bottom: 15px;
      text-align: center;
    }

    .menu {
      color: #495057;
    }

    .rating {
      font-weight: bold;
      color: #28a745;
    }

    .votes {
      font-size: 18px;
      color: #6c757d;
    }

    footer {
      margin-top: 20px;
      text-align: center;
      color: #adb5bd;
      font-size: 14px;
    }
  </style>
  <script>
    async function updateData() {
      try {
        const response = await fetch("/menu");
        const data = await response.json();
        document.getElementById("menu").innerText = `🍽️ Меню на сегодня: ${data.menu}`;
        document.getElementById("rating").innerText = `⭐ Рейтинг: ${data.rating}`;
        document.getElementById("votes").innerText = `✅ Вкусно: ${data.votes.good} | ❌ Не вкусно: ${data.votes.bad}`;
      } catch (error) {
        console.error("Ошибка загрузки данных", error);
      }
    }

    setInterval(updateData, 500); // Обновлять каждые пол секунд
    window.onload = updateData;
  </script>
</head>
<body>
  <div class="container">
    <h1>Мониторинг питания</h1>
    <div class="menu" id="menu">Загрузка меню...</div>
    <div class="rating" id="rating">Загрузка рейтинга...</div>
    <div class="votes" id="votes">Загрузка голосов...</div>
  </div>
  <footer>
    © 2024 ГБОУ "СОШ №4 с.п.Кантышево" | Поддержка: gbou_sosh_4_kantyshevo@mail.ru
  </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/menu', methods=['GET'])
def get_menu():
    today = datetime.now().weekday()
    menu = weekly_menu[today]
    total_votes = votes["good"] + votes["bad"]
    rating = f"{(votes['good'] / total_votes * 100):.1f}%" if total_votes > 0 else "Нет данных"
    return jsonify({"menu": menu, "rating": rating, "votes": votes})

@app.route('/vote', methods=['GET'])
def handle_vote():
    vote = request.args.get('vote')
    if vote in votes:
        votes[vote] += 1
        return jsonify({"status": "success", "votes": votes})
    return jsonify({"status": "error", "message": "Invalid vote"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
