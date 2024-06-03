void checkType(String stringtype, String stringdata)
{
    display.clear();
    
    if (stringtype == "00") {
        display.print("links");
        if(stringdata == "000000")
        {
          display.print("90*");
          Turn(2);
        }
        else{
        int result = binaryStringToInt(stringdata);
        display.print(result);
        GoLeft(stringdata, result);
        }
    } else if (stringtype == "01") {
        display.print("rechts");
        if(stringdata == "000000")
        {
          display.print("90*");
          Turn(1);
        }
        else{
        int result = binaryStringToInt(stringdata);
        display.print(result);
        GoRight(stringdata, result);
        }
    } else if (stringtype == "10") {
        display.print("rechtdoor");
        GoStraight();
    } else if (stringtype == "11") {
        display.print("verkeerbord");
        checkverkeersbord(stringdata);
    }
}
