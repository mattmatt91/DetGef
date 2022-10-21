void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("Enter data:");
  while (Serial.available() == 0) {}     //wait for data available
  String teststr = Serial.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String
  if (teststr == "red") {
    Serial.println("A primary color");
  } else {
    Serial.println("Something else");
  }
}