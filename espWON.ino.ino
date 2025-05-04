#include <WiFi.h>
#include <WebServer.h>
#include <M5Atom.h>


const char* ssid     = "IotPlayaBlanca";
const char* password = "kincetlos";


#define SWITCH1 22
WebServer server(80);


bool estadoRele = false;  // Estado del relé para control visual


void activarSwitch1() {
  Serial.println("[ESP32] Activando SWITCH1 (pulso 500ms)");
  digitalWrite(SWITCH1, HIGH);
  estadoRele = true;
  M5.dis.drawpix(0, 0xff0000);  // Rojo
  delay(500);
  digitalWrite(SWITCH1, LOW);
  estadoRele = false;
  M5.dis.drawpix(0, 0x00ff00);  // Verde
}


// Manejar la petición HTTP POST a /power
void handlePower() {
  activarSwitch1();
  server.send(200, "text/plain", "OK");
}


void setup() {
  M5.begin(true, false, true);
  M5.dis.drawpix(0, 0x00ff00);  // LED verde al inicio


  pinMode(SWITCH1, OUTPUT);
  digitalWrite(SWITCH1, LOW);


  Serial.begin(115200);
  WiFi.begin(ssid, password);


  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado. IP: " + WiFi.localIP().toString());


  server.on("/power", HTTP_POST, handlePower);
  server.begin();
  Serial.println("Servidor HTTP listo");
}


void loop() {
  M5.update();
  server.handleClient();


  if (M5.Btn.wasPressed()) {
    Serial.println("[ATOM] Botón presionado, encendiendo switch");
    activarSwitch1();
  }
}