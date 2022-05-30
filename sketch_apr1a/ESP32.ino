// Load Wi-Fi library

#include <WiFi.h>
//------------------------------
#include <ESP32Servo.h>
 
Servo servoIndex;  // create servo object to control a servo
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;
Servo servoThumb;
// 16 servo objects can be created on the ESP32
 
int pos = 0;    // variable to store the servo position
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 

int pinIndex = 18;
int pinThumb = 21;
int pinMiddle = 22;
int pinRing = 23;
int pinPinky = 32;
//--------------------------------

// Replace with your network credentials

const char* ssid = "Galaxy A4083EC";

const char* password = "mwlj7716";

//The udp library class

WiFiUDP udp;

unsigned int localUdpPort = 4210;  // local port to listen on

char incomingPacket[255];  // buffer for incoming packets

 char *  replyPacket = "Hi there! Got the message :-)";  // a reply string to send back

 char * broadcastPacket = "I am here";



void setup() {

  Serial.begin(9600);



  // Connect to Wi-Fi network with SSID and password

  Serial.print("Connecting to ");

  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");

  }

  // Print local IP address

  Serial.println("");

  Serial.println("WiFi connected.");

  Serial.println("IP address: ");

  Serial.println(WiFi.localIP());



  udp.begin(localUdpPort);

  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

//------------------------------------------
  // Allow allocation of all timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  servoIndex.setPeriodHertz(50);    // standard 50 hz servo
  servoMiddle.setPeriodHertz(50);    // standard 50 hz servo
  servoRing.setPeriodHertz(50);    // standard 50 hz servo
  servoPinky.setPeriodHertz(50);    // standard 50 hz servo
  servoThumb.setPeriodHertz(50);    // standard 50 hz servo
  servoIndex.attach(pinIndex); // attaches the servo on pin 18 to the servo object
  servoMiddle.attach(pinMiddle); // attaches the servo on pin 18 to the servo object
  servoRing.attach(pinRing); // attaches the servo on pin 18 to the servo object
  servoPinky.attach(pinPinky); // attaches the servo on pin 18 to the servo object
  servoThumb.attach(pinThumb); // attaches the servo on pin 18 to the servo object
  // using default min/max of 1000us and 2000us
  // different servos may require different min/max settings
  // for an accurate 0 to 180 sweep
//---------------------------------------------

}



unsigned long timer = 0;



void loop() {





  int packetSize = udp.parsePacket();

  if (packetSize)

  {

    // receive incoming UDP packets

//    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort();
//      Serial.print(incomingPacket);

      // WORKSPACE
//      for (int i = 0; i <= incomingPacket.length; i++) {
//        
//      }

      int index, middle, ring, pinky, thumb;
      sscanf(incomingPacket, "%d:%d:%d:%d:%d", &index, &middle, &ring, &pinky, &thumb);


      Serial.printf("%d, %d, %d, %d, %d", index, middle, ring, pinky, thumb);
      
      Serial.print("\n");

      //-------------------------------------
        servoIndex.write(index);
        servoMiddle.write(middle);
        servoRing.write(ring);
        servoPinky.write(pinky);
        servoThumb.write(thumb);
      //--------------------------------------------
                  
      // WORKSPACE END

    int len = udp.read(incomingPacket, 255);

    if (len > 0)

    {

      incomingPacket[len] = 0;

    }

//    Serial.printf("UDP packet contents: %s\n", incomingPacket);



    // send back a reply, to the IP address and port we got the packet from

    udp.beginPacket(udp.remoteIP(), udp.remotePort());

    udp.print(replyPacket);

    udp.endPacket();

  }
  
}
