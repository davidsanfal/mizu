#include <Servo.h> 

Servo leg_1_1, leg_1_2, leg_1_3;
Servo leg_2_1, leg_2_2, leg_2_3;
Servo leg_3_1, leg_3_2, leg_3_3;
Servo leg_4_1, leg_4_2, leg_4_3;
boolean stringComplete = false;
boolean startMessage = false;
int angle_1_1 = 0;
int angle_1_2 = 0;
int angle_1_3 = 0;

int angle_2_1 = 0;
int angle_2_2 = 0;
int angle_2_3 = 0;

int angle_3_1 = 0;
int angle_3_2 = 0;
int angle_3_3 = 0;

int angle_4_1 = 0;
int angle_4_2 = 0;
int angle_4_3 = 0;
String inputString = "";


void setup() 
{
  Serial.begin(115200);
  Serial.flush();
  leg_1_1.attach(2);
  leg_1_2.attach(3);
  leg_1_3.attach(4);
  
  leg_2_1.attach(5);
  leg_2_2.attach(6);
  leg_2_3.attach(7);

  leg_3_1.attach(8);
  leg_3_2.attach(9);
  leg_3_3.attach(10);

  leg_4_1.attach(11);
  leg_4_2.attach(12);
  leg_4_3.attach(13);
}

void loop() 
{
  /*String incoming;
  if (Serial.available()) incoming = read_string();
  if (stringComplete) {
    parse_string(incoming);
    stringComplete = false;

  leg_1_1.write(80 + angle_1_1);
  leg_1_2.write(80 - angle_1_2);
  leg_1_3.write(70 - angle_1_3);

  leg_2_1.write(80 + angle_2_1);
  leg_2_2.write(80 - angle_2_2);
  leg_2_3.write(70 - angle_2_3);

  leg_3_1.write(80 + angle_3_1);
  leg_3_2.write(80 - angle_3_2);
  leg_3_3.write(70 - angle_3_3);

  leg_3_1.write(80 + angle_4_1);
  leg_3_2.write(80 - angle_4_2);
  leg_3_3.write(70 - angle_4_3);
  }*/
  /*int val1 = map(analogRead(0), 0, 1023, 0, 179);
  int val2 = map(analogRead(1), 0, 1023, 0, 179);
  int val3 = map(analogRead(2), 0, 1023, 0, 179);
  leg_4_1.write(val1);
  leg_4_2.write(val2);
  leg_4_3.write(val3);
  Serial.print(val1);
  Serial.print("  ");
  Serial.print(val2);
  Serial.print("  ");
  Serial.println(val3);*/

  leg_1_1.write(93  + angle_1_1);
  leg_1_2.write(94 - angle_1_2);
  leg_1_3.write(60 - angle_1_3);

  leg_2_1.write(87 + angle_2_1);
  leg_2_2.write(80 - angle_2_2);
  leg_2_3.write(61 - angle_2_3);

  leg_3_1.write(82 + angle_3_1);
  leg_3_2.write(86 - angle_3_2);
  leg_3_3.write(65 - angle_3_3);

  leg_4_1.write(91 + angle_4_1);
  leg_4_2.write(95 - angle_4_2);
  leg_4_3.write(64 - angle_4_3);
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
        angle_1_1 = substr.toInt();
        substr = "";
      case 2:
        angle_1_2 = substr.toInt();
        substr = "";
      case 3:
        angle_1_3 = substr.toInt();
        substr = "";

      case 4:
        angle_2_1 = substr.toInt();
        substr = "";
      case 5:
        angle_2_2 = substr.toInt();
        substr = "";
      case 6:
        angle_2_3 = substr.toInt();
        substr = "";

      case 7:
        angle_3_1 = substr.toInt();
        substr = "";
      case 8:
        angle_3_2 = substr.toInt();
        substr = "";
      case 9:
        angle_3_3 = substr.toInt();
        substr = "";

      case 10:
        angle_4_1 = substr.toInt();
        substr = "";
      case 11:
        angle_4_2 = substr.toInt();
        substr = "";
      case 12:
        angle_4_3 = substr.toInt();
        substr = "";

      }
    }
    else substr += (char)inputString[i];
  }
  Serial.println(inputString);
}


