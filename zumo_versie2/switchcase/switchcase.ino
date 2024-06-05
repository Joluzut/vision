void checkType(String stringtype)
{
    display.clear();
    
    if (stringtype == "00") {
        display.print("links");
    } else if (stringtype == "01") {
        display.print("rechts");
    } else if (stringtype == "10") {
        display.print("rechtdoor");
    } else if (stringtype == "11") {
        display.print("verkeerbord");
    }
}