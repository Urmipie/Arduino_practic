// https://wokwi.com/projects/399861621760876545

const int photoPin = A0;
const int relPin = 2;
String serialinput;
int data;
int threshold;
bool modeOn, modeOff, relay, sensorOn, sensorOff, wasOn, wasOff;

/*
modeOn, modeOff - если True, то реле включается/выключается соответственно по свету, иначе только по команде с порта
relay - переменная, которая определяет состояние вкл/выкл
при подключении к com-порту режим работы и все параметры идут с него, иначе код сбрасывается в дефолтное состояние - вкл и выкл по освещению
wasOn, wasOff - показывают, был ли момент, когда реле соответветствовало состоянию освещения. служат для того, чтобы реле не переключалось моментально,
                если, лампа, например, была включена по времени ещё до того, как сенсор сказал её включить
*/

void setup() {
  relay = false;
  threshold = 100;
  modeOn = true;
  modeOff = true;

  wasOn = true;
  wasOff = true;

  Serial.begin(9600);
  pinMode(photoPin, INPUT);
  pinMode(relPin, OUTPUT);
  digitalWrite(relPin, HIGH);

  Serial.println('\n');
  Serial.println("connected:");
}

void loop() {
  if (Serial.available() > 0) {
    serialinput = Serial.readStringUntil(':');
    data = Serial.readStringUntil(';').toInt();

    if (serialinput == "sensorState") {
      Serial.println("sensorState:" + String(analogRead(photoPin)));
    }
    else if (serialinput == "setSensorThreshold")
    {
      threshold = data;
      Serial.println("ThresholdState:" + String(threshold));
    }
    else if (serialinput == "setModeOn") {
      wasOn = false;
      modeOn = data;
      Serial.println("modeOn:" + String(modeOn));
    }
    else if (serialinput == "setModeOff")
    {
      wasOff = false;
      modeOff = data;
      Serial.println("modeOff:" + String(modeOff));
    }
    else if (serialinput == "setRelay")
    {
      relay = data;
      Serial.println("setRelay:" + String(relay));
    }

  }
  sensorOn = analogRead(photoPin) < threshold + 1;
  sensorOff = analogRead(photoPin) > threshold - 1;

  wasOn = (sensorOn && relay) || wasOn;
  wasOff = (sensorOff && !relay) || wasOff;

  if (modeOn && sensorOn && wasOff)
  {
    relay = true;
  }
  else if (modeOff && sensorOff && wasOn)
  {
    relay = false;
  }


  if (relay){
    digitalWrite(relPin, HIGH);
  }
  else
  {
    digitalWrite(relPin, LOW);
  }
}
