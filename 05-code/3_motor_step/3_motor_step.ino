// #include <Servo.h>
// #include <Arduino.h>

unsigned char DHT = 0;
unsigned char DHN = 0;
int enPin = 8;
// Bas
int dirPin1 = 5;
int stepPin1 = 2;
#define limitX 9  // limit Base
// int SPx;

// Link 1
int dirPin2 = 6;
int stepPin2 = 3;
#define limitY 10  //limit Link 1
// int SPy;

// Link 2
int dirPin3 = 7;   // dirY
int stepPin3 = 4;  // stepY
#define limitZ 11  //limit Link 2
// int SPz;
// Link3
int namcham = 12;
// Servo myServo;
int dirPin3_TN = 0;

//CC
// int pinActuator = 13;
// int BLAC = 0;
//Base
float nStep1;
float drStep1 = 0.0;
float drStep1_old = 0.0;
float degree1 = 0.0;

//Link 1
float nStep2;
float drStep2 = 0.0;
float drStep2_old = 0.0;
float degree2 = 0.0;

//Link 2
//////////////////////////////khoi tao các biến ban đầu = 0
float nStep3;
float drStep3 = 0.0;
float drStep3_old = 0.0;
float degree3 = 0.0;

//Link 3
// int drNstep4 = 0;

String inChar = "";

// Variable global
String inString = " ";
String x1;
int delay1 = 1900; //1000
int delay2 = 1500; //5000
int delay3 = 1500; //500

int Xstate;
int Ystate;
int Zstate;

void runStep1(int nStepMotor1);
void Degree1(int dr, int dr_old);
void runStep2(int nStepMotor2);
void Degree2(int dr, int dr_old);
void runStep3(int nStepMotor3);
void Degree3(int dr, int dr_old);
void setHome();
void setup() {
  Serial.begin(9600);
  //
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(enPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin3, OUTPUT);
  pinMode(namcham,OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(limitX, INPUT_PULLUP);
  pinMode(limitY, INPUT_PULLUP);
  pinMode(limitZ, INPUT_PULLUP);
  digitalWrite(13, HIGH);
  digitalWrite(namcham,0);
  digitalWrite(enPin, 1);
}

void loop() {
  while (Serial.available()) 
  {
    String inChar = Serial.readString();
    // String inChar = Serial.readStringUntil('\n'); // Gán giá trị từ Serial vào biến toàn cục
    // inChar.trim();
    delayMicroseconds(1);
    Serial.println("Chuoi input:" + inChar);
    /////////////// SET HOME//////////////
    if (inChar[0] == 'S') 
    {
      drStep1 = 0;
      drStep2 = 0;
      drStep3 = 0;

      drStep1_old = 0.0;
      drStep2_old = 0.0;
      drStep3_old = 0.0;

      degree1 = 0.0;
      degree2 = 0.0;
      degree3 = 0.0;

      nStep1 = 0;
      nStep2 = 0;
      nStep3 = 0;
     digitalWrite(enPin,0);
     digitalWrite(dirPin1, 0);
     digitalWrite(dirPin2, 0);
     digitalWrite(dirPin3, 1); 
     setHome();
    }
    ///// STOP////////
    else if (inChar[0] == 'T') 
    {
      digitalWrite(enPin,1);
      drStep1 = 0;
      drStep2 = 0;
      drStep3 = 0;

      drStep1_old = 0.0;
      drStep2_old = 0.0;
      drStep3_old = 0.0;

      degree1 = 0.0;
      degree2 = 0.0;
      degree3 = 0.0;

      nStep1 = 0;
      nStep2 = 0;
      nStep3 = 0;
    }
    // else if (inChar[0] == 'X') {
    //   drStep2 = 0.0;
    //   Degree2(drStep2, drStep2_old);
    //   runStep2(nStep2);
    //   drStep2_old = drStep2;
    //   delay(1000);
    //   drStep1 = 90.0;
    //   Degree1(drStep1, drStep1_old);
    //   runStep1(nStep1);
    //   drStep1_old = drStep1;
    //   delay(1000);

    //   drStep3 = -90.0;
    //   Degree3(drStep3, drStep3_old);
    //   runStep3(nStep3);
    //   drStep3_old = drStep3;
    //   delay(1000);
    //   myServo.write(80);
    //   delay(300);
      
    //   digitalWrite(13, HIGH);
    //   delay(3000);

    //   drStep3 = 0.0;
    //   Degree3(drStep3, drStep3_old);
    //   runStep3(nStep3);
    //   drStep3_old = 0.0;
    //   delay(1000);
    //   myServo.write(80);
    //   drStep1 = 0.0;
    //   delay(300);
    //   Degree1(drStep1, drStep1_old);
    //   runStep1(nStep1);
    //   drStep1_old = 0.0;
    //   delay(1000);
    // } 
    // else if (inChar[0] == 'O') 
    // {
    //   x1 = inChar[1];
    //   BLAC = x1.toInt();
    //   if (BLAC == 1) {
    //     digitalWrite(13, LOW);
    //     delay(1000);
    //   } else {

    //     digitalWrite(13, HIGH);
    //     delay(1000);
    //   }
    // }
    ///////
    else if(inChar[0] == 'H')
      {
        Serial.println("Hut vat");
        // DHT = 0;
        // DHN = 0;
        digitalWrite(namcham,1);
        inString = "";
      }

      else if(inChar[0] == 'N')
      {
          Serial.println("Nha vat");
          // DHT = 0;
          // DHN = 0;
          digitalWrite(namcham,0);
          digitalWrite(enPin,0);
          inString = "";
      } 
    for (int x = 0; x < inChar.length(); x++) 
    {
      if ((inChar[x] == '-') || (inChar[x] == '.')) 
      {
        inString += (char)inChar[x];
      }
      if (isDigit(inChar[x])) 
      {
        inString += (char)inChar[x];
      }
     
      if (inChar[x] == 'A') 
      {
         delay(200);
        drStep1 = inString.toFloat();
        Degree1(drStep1, drStep1_old);
        runStep1(nStep1);
        drStep1_old = drStep1;
        inString = " ";
      } 
      
      else if (inChar[x] == 'B') 
      {
        drStep2 = inString.toFloat();
        delay(500);
        Degree2(drStep2, drStep2_old);
        runStep2(nStep2);
        drStep2_old = drStep2;
        inString = " ";
        delay(500);
      }

      else if (inChar[x] == 'C') 
      {
        delay(500); 
        drStep3 = inString.toFloat();
        inString = " ";
        Degree3(drStep3, drStep3_old);
        runStep3(nStep3);
        drStep3_old = drStep3;
        delay(500);
      }

      else if(inChar[x] == 'H')
      {
        Serial.println("Hut vat");
        // DHT = 0;
        // DHN = 0;
        digitalWrite(namcham,1);
        inString = "";
        delay(1000);
      }
      
      else if(inChar[x] == 'O')
      {
        Degree2(-30, drStep2_old);
        runStep2(nStep2);
        drStep2_old = -30;
          // delay(2000);
        Degree1(-87, drStep1_old);
        runStep1(nStep1);
        drStep1_old = -87;
          // delay(2000);
        Degree3(115, drStep3_old);
        runStep3(nStep3);
        drStep3_old = 115;
          delay(2000);
      }
      
      else if(inChar[x] == 'N')
      {
          Serial.println("Nha vat");
          // DHT = 0;
          // DHN = 0;
          digitalWrite(namcham,0);
          inString = "";
      } 
    }
  }
}
// Base
void runStep1(int nStepMotor1) 
{
  for (int x = 0; x < nStepMotor1; x++) 
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(delay1);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(delay1);
  }
}
void Degree1(int dr, int dr_old) 
{
  if (dr_old >= dr) 
  {
    digitalWrite(dirPin1, HIGH);
    degree1 = abs(dr - dr_old);
  } 
  else
  {
    digitalWrite(dirPin1, LOW);
    degree1 = abs(dr - dr_old);
  }
  nStep1 = degree1 * 200 * 4 *3.75 / 360;
}
// Link1
void runStep2(int nStepMotor2) 
{
  for (int x = 0; x < nStepMotor2; x++) 
  {
    digitalWrite(stepPin2, HIGH);
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(delay2);
    digitalWrite(stepPin2, LOW);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(delay2);
  }
}
void Degree2(int dr, int dr_old) 
{
  if (dr_old >= dr) 
  {
    digitalWrite(dirPin2, LOW);
    digitalWrite(dirPin3, HIGH);
    degree2 = abs(dr - dr_old);
    // dirPin3_TN = 0;
  } 
  else 
  {
    digitalWrite(dirPin2, HIGH);
    digitalWrite(dirPin3, LOW);
    degree2 = abs(dr - dr_old);
    // dirPin3_TN = 1;
  }
  // nStep2 = degree2 * 5 *8 / 3;
  nStep2 = degree2 * 200 * 3 * 8 / 360;
}
// Link2
void runStep3(int nStepMotor3) 
{
  for (int x = 0; x < nStepMotor3; x++) 
  {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(delay3);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(delay3);
  }
}
void Degree3(int dr, int dr_old) 
{
  if (dr_old >= dr) 
  {
    digitalWrite(dirPin3, HIGH);
    degree3 = abs(dr - dr_old);
  } 
  else 
  {
    digitalWrite(dirPin3, LOW);
    degree3 = abs(dr - dr_old);
  }
  // nStep3 = degree3 * 5 / 3;
  nStep3 = degree3 * 200 * 3 * 8 / 360;
}

void setHome()
{
    //STEP 1
  // if(drStep1_old >= 0)
  // {
  //   digitalWrite(dirPin1,1);
  //   for (int x=0; x<1000; x++)
  //   {
  //     Xstate = digitalRead(limitX);
  //     digitalWrite(stepPin1,HIGH); 
  //     delayMicroseconds(5000); 
  //     digitalWrite(stepPin1,LOW); 
  //     delayMicroseconds(5000);
  //     if (Xstate == LOW)
  //     {
  //       Serial.println("Touch sensor 1");
  //       break;
  //     }
  //   }
  // }
  // else
  // {
    
    for (int x=0; x<1000; x++)
    {
      Xstate = digitalRead(limitX);
      digitalWrite(stepPin1,HIGH); 
      delayMicroseconds(1300); 
      digitalWrite(stepPin1,LOW); 
      delayMicroseconds(1300);
      if (Xstate == LOW)
      {
        Serial.println("Touch sensor 1");
        break;
      }
    }
  // }
    //STEP 2
  while (digitalRead(limitY) == HIGH) 
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(650); // Điều chỉnh tốc độ
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(650);

    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(650);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(650);
  }
  delay(10); // Đợi để debounce
  Serial.println("Touch sensor 2");

  digitalWrite(dirPin2, 1);
  digitalWrite(dirPin3, 0);
  for (int y = 0; y < (318*8); y++) //324
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(650); //5000
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(650);

    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(1650);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(1650); //6000
  }
    // STEP 3
  digitalWrite(dirPin3, 1);
  while (digitalRead(limitZ) == HIGH) 
  {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(700); // Điều chỉnh tốc độ //5000
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(700);
  }

  // Khi chạm công tắc hành trình
  Serial.println("Touch sensor 3");

  // Đảo chiều động cơ
  digitalWrite(dirPin3, 0);

  for (int y = 0; y < (170*8); y++) 
  {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(700);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(700);
  }
}
