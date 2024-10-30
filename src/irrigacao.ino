#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 15  // Pino onde o DHT22 está conectado
#define DHTTYPE DHT22

// Definir os pinos dos botões e LDR
#define BOTAO_P 12   // Sensor de nutrientes P
#define BOTAO_K 13   // Sensor de nutrientes K
#define LDR_PIN 34   // Usando GPIO 34 para o pino analógico do LDR

// Definir o pino do relé
#define RELE_PIN 14  // Pino do relé

DHT dht(DHTPIN, DHTTYPE);

// Definindo parâmetros
const float UMIDADE_MINIMA = 50.0; // Umidade mínima para ativar irrigação
const float pH_MIN = 6.0;          // Valor mínimo de pH
const float pH_MAX = 8.0;          // Valor máximo de pH

// Definir credenciais de Wi-Fi e URL do servidor
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* serverUrl = "http://192.168.15.78:5000/inserir_dados";  // Substitua pelo IP do servidor

void setup() {
  Serial.begin(115200);

  // Conectar ao Wi-Fi com timeout
  WiFi.disconnect(true);  // Limpa configurações salvas
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
      delay(1000);
      Serial.print(".");
      tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
      Serial.println(" Conectado ao WiFi!");
  } else {
      Serial.println(" Falha ao conectar ao WiFi.");
      return;
  }

  // Inicializar os pinos dos botões e do relé
  pinMode(BOTAO_P, INPUT_PULLUP);
  pinMode(BOTAO_K, INPUT_PULLUP);
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, LOW);

  // Inicializar o sensor DHT22
  dht.begin();
}

void enviarDados(float umidade, float temperatura, float nivelpH, bool estadoP, bool estadoK, bool irrigacaoAtiva) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);

        // Formatar dados em JSON
        String jsonPayload = "{\"umidade\": " + String(umidade) +
                             ", \"temperatura\": " + String(temperatura) +
                             ", \"pH\": " + String(nivelpH) +
                             ", \"P\": " + String(estadoP) +
                             ", \"K\": " + String(estadoK) +
                             ", \"irrigacaoAtiva\": " + String(irrigacaoAtiva) + "}";

        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST(jsonPayload);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Resposta do servidor: " + response);
        } else {
            Serial.print("Erro ao enviar dados. Código de erro: ");
            Serial.println(httpResponseCode);
        }
        http.end();
    } else {
        Serial.println("WiFi desconectado. Dados não enviados.");
    }
}

void loop() {
  // Ler os valores dos botões
  bool estadoP = digitalRead(BOTAO_P) == LOW;
  bool estadoK = digitalRead(BOTAO_K) == LOW;

  // Ler o valor do LDR (simulando o pH) no GPIO 34
  int valorLDR = analogRead(LDR_PIN);
  float nivelpH = map(valorLDR, 0, 4095, 0, 14);

  // Ler umidade e temperatura do DHT22
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  if (isnan(umidade) || isnan(temperatura)) {
      Serial.println("Falha ao ler do DHT!");
      return;
  }

  // Mostrar valores no monitor serial
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");
  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println("%");
  Serial.print("Nutriente P: ");
  Serial.println(estadoP ? "Detectado" : "Não detectado");
  Serial.print("Nutriente K: ");
  Serial.println(estadoK ? "Detectado" : "Não detectado");
  Serial.print("pH: ");
  Serial.println(nivelpH);
  Serial.println("-----------------------");

  // Lógica para controle da irrigação
  bool irrigacaoAtiva = (umidade < UMIDADE_MINIMA || estadoP || estadoK || nivelpH < pH_MIN || nivelpH > pH_MAX);
  digitalWrite(RELE_PIN, irrigacaoAtiva ? HIGH : LOW);
  Serial.println(irrigacaoAtiva ? "Irrigação LIGADA" : "Irrigação DESLIGADA");

  // Enviar dados para o servidor
  enviarDados(umidade, temperatura, nivelpH, estadoP, estadoK, irrigacaoAtiva);

  delay(2000);  // Intervalo de 2 segundos entre leituras
}
