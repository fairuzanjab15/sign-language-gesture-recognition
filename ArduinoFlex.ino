const int jempol = A0; //Pin input untuk jempol
const int telunjuk = A1;
const int tengah = A2;
const int manis = A3;
const int klgk = A4;


int jl = 0;
int tl = 0;
int th = 0;
int ms = 0;
int kl = 0;

void setup(){
  Serial.begin(115200);
  pinMode(jempol, INPUT);
  pinMode(telunjuk, INPUT);
  pinMode(tengah, INPUT);
  pinMode(manis, INPUT);
  pinMode(klgk, INPUT);
  
  delay(200);
}

void loop(){
  
  //JEMPOL
  jl = analogRead(jempol);
  Serial.print(jl);

  //TELUNJUK
  Serial.print(',');
  tl = analogRead(telunjuk);
  Serial.print(tl);

  //TENGAH
  Serial.print(',');
  th = analogRead(tengah);
  Serial.print(th);

  //MANIS
  Serial.print(',');
  ms = analogRead(manis);
  Serial.print(ms);

  //KELINGKING
  Serial.print(',');
  kl = analogRead(klgk);
  Serial.println(kl);
  
  delay(100);
}
