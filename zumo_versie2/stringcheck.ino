void checkType(String stringtype, String stringdata)
{
    
    if (stringtype == "00") {// check turn left
       // display.print("links");
        if(stringdata == "000000")
        {
         display.print("90*");
          Turn(2);
        }
        else{
        int result = binaryStringToInt(stringdata);
        //display.print(result);
        GoLeft(stringdata, result);
        }
    } else if (stringtype == "01") {// check for turn right
       // display.print("rechts");
        if(stringdata == "000000")
        {
          display.print("90*");
          Turn(1);
        }
        else{
        int result = binaryStringToInt(stringdata);
       // display.print(result);
        GoRight(stringdata, result);
        }
    } else if (stringtype == "10") {// check for straight
     //   display.print("rechtdoor");
     if(stringdata == "000000")
     {
      stopmoving();
     }
     else{
        GoStraight();
     }
    
    } else if (stringtype == "11") {// check for trafficbord and traffic light
        display.print("verkeerbord");
        checkverkeersbord(stringdata);
    }
}
