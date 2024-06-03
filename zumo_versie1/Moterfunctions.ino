void GoStraight(){
  for (int speed = 0; speed <= 50; speed++)
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}
void GoLeft(String stringdata, int result)
{
    ledYellow(0);
   for (int speed = 50; speed <= 150; speed++)
  {
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
  delay(result * 10);
      ledYellow(0);

   for (int speed = 150; speed >= 50; speed--)
  {
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}

void GoRight(String stringdata, int result)
{
  for (int speed = 50; speed <= 150; speed++)
  {
    motors.setLeftSpeed(speed);
    delayMicroseconds(100);
  }
  delay(result * 10);
      ledYellow(0);

      ledYellow(0);
  for (int speed = 150; speed >= 50; speed--)
  {
    motors.setLeftSpeed(speed);
    delayMicroseconds(100);
  }
}

void Turn(int turn)

{
  int left = 0;
  int right = 0;
  if(turn == 1)
  {
left = 1;
right = -1;
  }
  else
  {
     left = -1;
     right = 1;
  }
  //flowrizz is jong  
    for (int speed = 50; speed <= 150; speed++)
  {
    motors.setLeftSpeed(speed * left);
     motors.setRightSpeed(speed * right);
    delayMicroseconds(100);
  }
  delay(540);
      ledYellow(0);

      ledYellow(0);
  for (int speed = 150; speed >= 50; speed--)
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}