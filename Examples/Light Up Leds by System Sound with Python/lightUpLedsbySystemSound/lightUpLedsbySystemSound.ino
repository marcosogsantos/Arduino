// set pin address to led names
int led0 = 3;
int led1 = 4;
int led2 = 5;
int led3 = 6;
int led4 = 7;
int led5 = 8;
int led6 = 9;
int led7 = 10;
int led8 = 12;
int led9 = 13;

// group all leds in one array
int pins[] = {led0,led1,led2,led3,led4,led5,led6,led7,led8,led9};

// set first led to serial input synchronization
int actualPinIndex = 0;

// set final message as global var
String finalMessage;

// set last incoming byte as global var
char incomingByte;

void setup() {
  // put your setup code here, to run once:

  // open serial comunication
  Serial.begin(9600);

  // light up all leds
  for (int pin = 0; pin < sizeof(pins); pin++){
    pinMode(pin,OUTPUT);
    digitalWrite(pin, HIGH);
  }
  
} 

void loop() { 
  // put your main code here, to run repeatedly:

  // check if have some byte to receive from serial port
  if (Serial.available()>0){

    // read last incoming byte  
    incomingByte = Serial.read();

    // merge byte string to final message var
    finalMessage = String( finalMessage + String(incomingByte));
    
    // ligh up led if byte string its equal "1" otherwise turn off
    if (String(incomingByte) == "1"){
      digitalWrite(pins[actualPinIndex],HIGH);
    } else {
      digitalWrite(pins[actualPinIndex],LOW);
    }

    // go to next pin
    actualPinIndex++;
    
    // find message end
    if (String(incomingByte) == ";"){
      // back to first led
      actualPinIndex=0;

      // send final message back
      Serial.println(finalMessage);

      // reset message var
      finalMessage = "";
    }
    
  }
 }
