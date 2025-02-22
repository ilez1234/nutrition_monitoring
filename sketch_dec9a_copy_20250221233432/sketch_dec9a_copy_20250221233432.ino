#include <WiFi.h>
#include <HTTPClient.h>

// Настройки Wi-Fi
const char* ssid = "12";
const char* password = "12345678";

// URL вашего сервера
const char* serverURL = "http://192.168.41.243:5000/vote";

// Пины кнопок
const int buttonGood = 12; // GPIO12
const int buttonBad = 14;  // GPIO14

// Переменные для отслеживания состояния кнопок
bool lastStateGood = HIGH;
bool lastStateBad = HIGH;

void setup() {
  Serial.begin(115200);

  // Настройка пинов кнопок
  pinMode(buttonGood, INPUT_PULLUP);
  pinMode(buttonBad, INPUT_PULLUP);

  // Подключение к Wi-Fi
  Serial.print("Подключение к Wi-Fi ");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi подключен");
  Serial.print("IP-адрес: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Проверяем кнопку "Вкусно"
  bool currentStateGood = digitalRead(buttonGood);
  if (currentStateGood == LOW && lastStateGood == HIGH) {
    Serial.println("Кнопка 'Вкусно' нажата");
    sendVote("good");
  }
  lastStateGood = currentStateGood;

  // Проверяем кнопку "Не вкусно"
  bool currentStateBad = digitalRead(buttonBad);
  if (currentStateBad == LOW && lastStateBad == HIGH) {
    Serial.println("Кнопка 'Не вкусно' нажата");
    sendVote("bad");
  }
  lastStateBad = currentStateBad;

  delay(100); // Защита от дребезга кнопок
}

// Функция для отправки голоса на сервер
void sendVote(const char* voteType) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Формируем URL с параметром
    String url = String(serverURL) + "?vote=" + voteType;

    http.begin(url); // Инициализируем запрос
    int httpCode = http.GET(); // Отправляем GET-запрос

    // Проверяем ответ сервера
    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Ответ сервера: " + payload);
    } else {
      Serial.println("Ошибка подключения: " + String(http.errorToString(httpCode).c_str()));
    }

    http.end(); // Завершаем запрос
  } else {
    Serial.println("Wi-Fi не подключён");
  }
}
