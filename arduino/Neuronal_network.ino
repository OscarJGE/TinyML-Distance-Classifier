const int ECO = 9;
const int TRIG = 10;
const int U28015 = 11;
const float pesos[] = {-0.017007, -0.007949, -0.015043};
const float bias[] = {0.194594, 0.170519, 0.468311};
long duracion, distancia;
int act_n1, act_n2;
int act_n[3];
float n[3];


void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECO, INPUT);
  pinMode(U28015, INPUT);
}

void loop() {
  //DEPENDIENDO DEL SENSOR QUE UTILICES SELECCIONA LA OPCION DE 1 o 2 PINES
  //medir_distancia_SR04();
  medir_distancia_28015(U28015);

  for(int i = 0; i < 3; i++){
    // La fórmula estándar: n = (w * x) + b
    n[i] = (pesos[i] * distancia) + bias[i];
    activacion(i);
  }

  //Variables de JSON
  String etiqueta = "";
  int key = 0;
 
  //Decodificador manual
  if (act_n[0] == 1 && act_n[1] == 1 && act_n[2] == 1){
    etiqueta = "Muy cerca...";
    key = 1;
  } else if (act_n[0] == 0 && act_n[1] == 1 && act_n[2] == 1){
    etiqueta = "Casi cerca...";
    key = 2;
  } else if (act_n[0] == 0 && act_n[1] == 0 && act_n[2] == 1){
    etiqueta = "Rango normal...";
    key = 3;
  } else if (act_n[0] == 0 && act_n[1] == 0 && act_n[2] == 0){
    etiqueta = "Lejos...";
    key = 4;
  } else {
    etiqueta = "Calculando..."; 
    key = 4; 
  }

  // Imprimimos todo junto para que no se rompa la cadena
  Serial.print("{");
  Serial.print("\"distancia\": "); Serial.print(distancia);
  Serial.print(", ");
  Serial.print("\"etiqueta\": \""); Serial.print(etiqueta); Serial.print("\"");
  Serial.print(", ");
  Serial.print("\"key\": "); Serial.print(key);
  Serial.println("}"); // Fin del JSON

  delay(100);
}

//Medición del sensor ultrasonico HC-SR04
void medir_distancia_SR04(){
  digitalWrite(TRIG, HIGH);
  delay(1);
  digitalWrite(TRIG, LOW);
  duracion = pulseIn(ECO, HIGH);
  distancia = duracion / 58.2;
}

//Medición del sensor ultrasonico 28015
void medir_distancia_28015(int pin){
  // Lo convertimos en SALIDA para disparar el pulso
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  digitalWrite(pin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pin, LOW);

  // 2. Lo convertimos en ENTRADA para escuchar el eco
  pinMode(pin, INPUT);
  long tiempo = pulseIn(pin, HIGH);
  distancia = tiempo / 58.2;
}



// Función Escalón
void activacion(int indice){
  if (n[indice] >= 0.0){
    act_n[indice] = 1;
  }else{
    act_n[indice] = 0;
  }
}
