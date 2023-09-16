#define numOfValsRec 2
#define digitsPerValRec 1

int valsRec[numOfValsRec];
int stringLength = digitsPerValRec * numOfValsRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;

void receivedData() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      counterStart = true;
    }
    if (counterStart) {
      if (counter < stringLength) {
        receivedString = String(receivedString + c);
        counter++;
        if (counter >= stringLength) {
          for (int i = 0; i < numOfValsRec; i++) {
            int num = (i * digitsPerValRec) + 1;
            valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
          }
          receivedString = "";
          counter = 0;
          counterStart = false;
        }
      }
    }
  }
}


void setup() {
  pinMode(6, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  receivedData();
  if (valsRec[0] == 1) {
    digitalWrite(6, 1);
    delay(500);
    digitalWrite(6, 0);
    delay(500);
    
  }
  else {
    digitalWrite(6, 0);
  }
}
