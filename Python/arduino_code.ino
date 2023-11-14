#include <Wire.h>
#include <CytronMotorDriver.h>

CytronMD motor1(PWM_DIR, 3, 4);

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }

  // Generate random current and magnetometer readings (replace with actual sensor readings)
  float current = random(0, 10) + random(0, 100) * 0.01;
  float magnetometer = random(-180, 180) + random(0, 100) * 0.01;

  Serial.print("C:");
  Serial.print(current);
  Serial.print(",M:");
  Serial.println(magnetometer);

  delay(1000); 
}

void processCommand(String command) {
  if (command.startsWith("S:")) {
    int speed = command.substring(2).toInt();
    motor1.setSpeed(speed);
  }
}

