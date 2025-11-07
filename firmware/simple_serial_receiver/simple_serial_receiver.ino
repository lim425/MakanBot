void setup() {
  Serial.begin(9600);
  Serial.println("Initialized");
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command != '\n'){
      switch (command) {
      case 'A':
        Serial.println("Received: A");
        break;
      case 'B':
        Serial.println("Received: B");
        break;
      case 'C':
        Serial.println("Received: C");
        break;
      case 'D':
        Serial.println("Received: D");
        break;
      case 'E':
        Serial.println("Received: E");
        break;
      case 'F':
        Serial.println("Received: F");
        break;
      case 'G':
        Serial.println("Received: G");
        break;
      case 'H':
        Serial.println("Received: H");
        break;
      case 'I':
        Serial.println("Received: I");
        break;
      case 'X':
        Serial.println("Received: X");
        break;
      case 'Z':
        Serial.println("Received: Z");
        break;
      default:
        Serial.println("Type A to Z");
        break;
      }
    }
  }
}
