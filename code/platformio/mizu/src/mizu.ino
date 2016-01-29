#include <Servo.h> 

Servo leg_1_1, leg_1_2, leg_1_3;
Servo leg_2_1, leg_2_2, leg_2_3;
Servo leg_3_1, leg_3_2, leg_3_3;
Servo leg_4_1, leg_4_2, leg_4_3;

int input[12];
byte inputAux[14];


void setup() 
{
  Serial.begin(19200);
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
  if (Serial.available()){
    read_message();
    for(int a=0 ; a<12; a++){
      Serial.print((int)input[a]);
      Serial.print(" , ");
    }
    Serial.println("");
    leg_1_1.write(93  + (int)input[0]);
    leg_1_2.write(94 - (int)input[1]);
    leg_1_3.write(60 - (int)input[2]);

    leg_2_1.write(87 + (int)input[3]);
    leg_2_2.write(80 - (int)input[4]);
    leg_2_3.write(61 - (int)input[5]);

    leg_3_1.write(82 + (int)input[6]);
    leg_3_2.write(86 - (int)input[7]);
    leg_3_3.write(65 - (int)input[8]);

    leg_4_1.write(91 + (int)input[9]);
    leg_4_2.write(95 - (int)input[10]);
    leg_4_3.write(64 - (int)input[11]);
  }
}

void read_message() {
  while (Serial.available()) {
    Serial.readBytes(inputAux, 14);
    if(inputAux[0] == 190 && inputAux[13] == 192){
      for(int a=1 ; a<13; a++){
        input[a-1] = inputAux[a]-90;
      }
    }
  }
}