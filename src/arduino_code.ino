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
  mag_field_x = magnetometer.getX() * -1;
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
  // Split the command string by commas to separate commands for X, Y, and Z.
  int index1 = command.indexOf(",");
  int index2 = command.lastIndexOf(",");

  String cmd1 = command.substring(0, index1);
  String cmd2 = command.substring(index1+1, index2);
  String cmd3 = command.substring(index2+1);

  int speed_x = cmd1.substring(2).toInt();
  int speed_y = cmd2.substring(2).toInt();
  int speed_z = cmd3.substring(2).toInt();

  int speeds[3] = {speed_x, speed_y, speed_z};

  for (int i = 0; i < 3; i++) {
    if (speeds[i] > 100) speeds[i] = 100;
    if (speeds[i] < -100) speeds[i] = -100;
  }

  driver_x.setSpeed(speeds[0]);
  driver_y.setSpeed(speeds[1]);
  driver_z.setSpeed(speeds[2]);
}
