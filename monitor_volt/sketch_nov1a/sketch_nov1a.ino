void setup() {
    Serial.begin(9600); // Start serial communication at 9600 bps
}

void loop() {
    int sensorValueA0 = analogRead(A0); // Read from A0
    int sensorValueA1 = analogRead(A1); // Read from A1

    // Convert the analog reading (0-1023) to voltage (0-5V)
    float voltageA0 = sensorValueA0 * (5.0 / 1023.0);
    float voltageA1 = sensorValueA1 * (5.0 / 1023.0);

    // Send the voltages to the serial port with precision
    Serial.print(voltageA0, 2); // 2 decimal places for voltageA0
    Serial.print(",");
    Serial.println(voltageA1, 2); // 2 decimal places for voltageA1

    delay(1000); // Wait for a second before the next reading
}
