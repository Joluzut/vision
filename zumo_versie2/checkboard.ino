void checkverkeersbord(String data)
{

if(data == "000000")
{
    display.clear();
}
else if(data == "000001")// code voor het driehoekig voorangsbord
{
    display.clear();
    display.print("voorang");
    display.gotoXY(0, 1);
    display.print("geven");

}
else if(data == "000010")// code for 
{
      display.clear();
    display.print("voorang");
    display.gotoXY(0, 1);
    display.print("nemen");
}
else if(data == "000100")
{
      display.clear();
    display.print("verboden");
    display.gotoXY(0, 1);
    display.print("toegang");
}
else if(data == "000011")
{
   display.clear();
      display.print("STOP");
    for (int speed = 50; speed >= 0; speed--)
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
  delay(500);
  for (int speed = 0; speed <= 50; speed++)
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delayMicroseconds(100);
  }
}
else if(data == "000101")//groen
{
   display.clear();
      display.print("Groen");
}
else if(data == "000110")// orangje
{
   display.clear();
      display.print("oranje");
}
else if(data == "000111")// rood
{
   display.clear();
      display.print("Rood");
}
}