// pins for
// valve #      1  2  3  4  5
int valves[] = {2, 3, 4, 5, 6};
int states[] = {LOW, LOW, LOW, LOW, LOW};

void setup() {
  for (byte i = 0; i < 5; i = i + 1) {
    pinMode(valves[i], OUTPUT);
    digitalWrite(valves[i], LOW);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String in_str = Serial.readStringUntil('#');
    if (!in_str.startsWith("@")) {
      send_message_format_error();
      return;
    }
    int dot1 = in_str.indexOf('.');
    int dot2 = in_str.lastIndexOf('.');
    if (dot1 == -1 || dot2 == -1 || dot1 == dot2) {
      send_message_format_error();
      return;
    }
    String command = in_str.substring(1, dot1);
    String dev_num_str = in_str.substring(dot1+1, dot2);
    long dev_num = dev_num_str.toInt();
    if (dev_num < 1 || dev_num > 5) {
      send_wrong_devnum_error();
      return;
    }
    String value = in_str.substring(dot2+1);
    if (command.equals("HSH")) {
      if (!value.equals("NISMF")) {
        send_wrong_handshake_error();
        return;
      } else {
        Serial.write("@HSH.DBQWT#");
      }
    } else if (command.equals("GET")) {
      if (states[dev_num-1] == LOW) {
        Serial.write("@ANS.CLOSE#");
      } else {
        Serial.write("@ANS.OPEN#");
      }
    } else if (command.equals("SET")) {
      if (value.equals("OPEN")) {
        digitalWrite(valves[dev_num-1], HIGH);
        states[dev_num-1] = HIGH;
        Serial.write("@OK.OPEN#");
      } else if (value.equals("CLOSE")) {
        digitalWrite(valves[dev_num-1], LOW);
        states[dev_num-1] = LOW;
        Serial.write("@OK.CLOSE#");
      } else {
        send_wrong_value_error();
        return;
      }
    }
  }
}

void send_message_format_error() {
  Serial.write("@ERR.MSGFMT#");
}

void send_wrong_devnum_error() {
  Serial.write("@ERR.DVNM#");
}

void send_wrong_handshake_error() {
  Serial.write("@ERR.HNDSHK#");
}

void send_wrong_value_error() {
  Serial.write("@ERR.VL#");
}
