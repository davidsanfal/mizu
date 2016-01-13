#include <Servo.h> 

Servo s1, s2, s3;
boolean stringComplete = false;
boolean startMessage = false;
int angle_0 = 0;
int angle_1 = 0;
int angle_2 = 0;
String inputString = "";


void setup() 
{
  Serial.begin(115200);
  Serial.flush();
  s1.attach(9);
  s2.attach(10);
  s3.attach(11);
}

void loop() 
{
  String incoming;
  if (Serial.available()) incoming = read_string();
  if (stringComplete) {
    parse_string(incoming);
    stringComplete = false;

  s1.write(80 + angle_0);
  s2.write(80 - angle_1);
  s3.write(70 - angle_2);
  }
}

String read_string() {
  char inChar;
  while (Serial.available()) {
    inChar = (char)Serial.read();
    if (inChar == ')') {
      startMessage = false;
      stringComplete = true;
      inputString += ',';
    }
    if (startMessage) inputString += inChar;
    if (inChar == '(' && !startMessage) startMessage = true;
    if (inChar == '(' && startMessage) inputString = "";
    delay(1);
    if (stringComplete) break;
  }
  return inputString;
}


void parse_string(String inputString) {
  int message_substring = 0;
  String substr = "";
  for (int i = 0 ; i < inputString.length(); i++) {
    if (inputString[i] == ',') {
      message_substring++;
      switch (message_substring) {
      case 1:
        angle_0 = substr.toInt();
        substr = "";
      case 2:
        angle_1 = substr.toInt();
        substr = "";
      case 3:
        angle_2 = substr.toInt();
        substr = "";
      }
    }
    else substr += (char)inputString[i];
  }
  Serial.println(inputString);
}


