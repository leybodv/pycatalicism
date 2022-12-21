// pins for
// valve #      1  2  3  4  5
int valves[] = {2, 3, 4, 5, 6};

void setup() {
  for (byte i = 0; i < 5; i = i + 1) {
    pinMode(valves[i], OUTPUT);
    digitalWrite(valves[i], LOW);
  }
  Serial.begin(9600);
}

void loop() {
  int in_byte;
  String in_str;
  if (Serial.available() > 0) {
    in_byte = Serial.read();
    if (in_byte != '@') {
      send_message_format_error();
    }
  in_str = Serial.readStringUntil('#');
  dot_index = in_str.indexOf('.');
  }
}

void send_message_format_error() {
}
