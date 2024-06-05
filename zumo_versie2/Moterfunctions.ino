void GoStraight(){// zet the speed of the motors to 50
    int speed = 50;
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
}
void GoLeft(String stringdata, int result)//go left by the amount that is given by the nicla
{
    ledYellow(0);
   for (int speed = 50; speed <= 200; speed++)
  {
    motors.setRightSpeed(speed);// increase the speed of the right motor linearly
    delayMicroseconds(100);
  }
  delay(result * 5);// for this amount left
      ledYellow(0);

   for (int speed = 200; speed >= 50; speed--)
  {
    motors.setRightSpeed(speed);// decrease the speed of the right moter linearly
    delayMicroseconds(100);
  }
}

void GoRight(String stringdata, int result)//go right by the amount that is given by the nicla
{
  for (int speed = 50; speed <= 200; speed++)
  {
    motors.setLeftSpeed(speed);//increase the speed of the left moter linearly
    delayMicroseconds(100);
  }
  delay(result * 5);
      ledYellow(0);

      ledYellow(0);
  for (int speed = 200; speed >= 50; speed--)
  {
    motors.setLeftSpeed(speed);//decrease the speed of the left moter linearly
    delayMicroseconds(100);
  }
}

void Turn(int turn)// make a 90 degree turn left or right

{
  int left = 0;
  int right = 0;
  if(turn == 1)// turn right
  {
          display.clear();
    display.print("90right");
left = 1;
right = -1;
  }
  else // turn left
  {
          display.clear();
    display.print("90left");
     left = -1;
     right = 1;
  }

    for (int speed = 50; speed <= 150; speed++)//increase te speed of one side and decrease the other
  {
    motors.setLeftSpeed(speed * left);
     motors.setRightSpeed(speed * right);
    delayMicroseconds(100);
  }
  delay(540);
      ledYellow(0);

      ledYellow(0);
  for (int speed = 150; speed >= 50; speed--)//set speed of the motors to 50
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}
void stopmoving()
{
    for (int speed = 50; speed >= 0; speed--)//set speed of the motors to 50
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}
