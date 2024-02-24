#include <ACS712.h>

#include <Wire.h>
#include <CytronMotorDriver.h>
#include "ACS712.h"
#include <QMC5883LCompass.h>

// Sensors
ACS712 curr_sens_x(A0, 5.0, 1023, 100);
QMC5883LCompass magnetometer;

// Configure the H-bridges
CytronMD driver_x(PWM_DIR, 3, 4);  // PWM = Pin 3, DIR = Pin 4.

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
  curr_y = 0;
  curr_z = 0;

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
  if (command.startsWith("S:")) {
    int speed = command.substring(2).toInt();
    if (speed > 50) speed = 50;
    driver_x.setSpeed(speed);
  }
}
