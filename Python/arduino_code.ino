#include <ACS712.h>

#include <Wire.h>
#include <CytronMotorDriver.h>
#include "ACS712.h"
#include <QMC5883LCompass.h>

// Sensors
ACS712 curr_sens_x(A0, 5.0, 1023, 100);
ACS712 curr_sens_y(A2, 5.0, 1023, 100);
ACS712 curr_sens_z(A1, 5.0, 1023, 100);
QMC5883LCompass magnetometer;

// Configure the H-bridges
CytronMD driver_x(PWM_DIR, 3, 4);  // PWM = Pin 3, DIR = Pin 4.
CytronMD driver_y(PWM_DIR, 6, 7)`;  // PWM = Pin 6, DIR = Pin 7.
CytronMD driver_z(PWM_DIR, 9, 8);  // PWM = Pin 6, DIR = Pin 7.

// Readings
int mag_field_x, mag_field_y, mag_field_z;
int curr_x, curr_y, curr_z;

void setup() {
  // Init
  Serial.begin(9600);
  Wire.begin();
  magnetometer.init();

  // Get these values from calibrate ino
  magnetometer.setCalibrationOffsets(-461.00, -1292.00, -181.00);
  magnetometer.setCalibrationScales(1.27, 0.87, 0.93);
  magnetometer.setSmoothing(10, true);

  // Calibrate current sensor (make sure current = 0)
  curr_sens_x.autoMidPointDC(100);
  curr_sens_y.autoMidPointDC(100);
  curr_sens_z.autoMidPointDC(100);
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }

  // Magnetometer
  magnetometer.read();
  // Return XYZ readings
  mag_field_x = magnetometer.getX();
  mag_field_y = magnetometer.getY();
  mag_field_z = magnetometer.getZ();

  // Current Sensor
  curr_x = curr_sens_x.mA_DC(100);
  curr_y = curr_sens_y.mA_DC(100);
  curr_z = curr_sens_z.mA_DC(100);;

  Serial.print("CX:");
  Serial.print(curr_x);
  Serial.print(",CY:");
  Serial.print(curr_y);
  Serial.print(",CZ:");
  Serial.print(curr_z);
  Serial.print(",X:");
  Serial.print(mag_field_x);
  Serial.print(",Y:");
  Serial.print(mag_field_y);
  Serial.print(",Z:");
  Serial.println(mag_field_z);

  delay(100);
}

void processCommand(String command) {
  if (command.startsWith("X:")) {
    int speed_x = command.substring(2).toInt();
    if (speed > 25) speed = 25;
    if (speed < -25) speed = -25;
    driver_x.setSpeed(speed);
  }  else if (command.startsWith("Y:")) {
    int speed_y = command.substring(2).toInt();
    if (speed > 25) speed = 25;
    if (speed < -25) speed = -25;
    driver_y.setSpeed(speed);
  }  else if (command.startsWith("Z:")) {
    int speed_z = command.substring(2).toInt();
    if (speed > 25) speed = 25;
    if (speed < -25) speed = -25;
    driver_z.setSpeed(speed);
  } else {
    Serial.println("Invalid command");
  }
}

void processCommand(String command) {
  // Split the command string by commas to separate commands for X, Y, and Z.
  String[] commands = command.split(",");
  for (String individualCommand : commands) {
    // Split each command by the colon to separate the axis from its speed value.
    String[] parts = individualCommand.split(":");
    if (parts.length == 2) {
      String axis = parts[0];
      int speed = Integer.parseInt(parts[1]);

      // Constrain the speed values.
      if (speed > 100) speed = 100;
      if (speed < -100) speed = -100;

      // Apply the speed to the correct axis.
      switch (axis) {
        case "X":
          driver_x.setSpeed(speed);
          break;
        case "Y":
          driver_y.setSpeed(speed);
          break;
        case "Z":
          driver_z.setSpeed(speed);
          break;
        default:
          Serial.println("Invalid command: " + axis);
          break;
      }
    } else {
      Serial.println("Invalid command format");
    }
  }
}
