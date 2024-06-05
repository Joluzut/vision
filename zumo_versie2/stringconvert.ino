int binaryStringToInt(String binaryString) {
  // Convert String to C-style string
  const char *cstr = binaryString.c_str();

  // Use strtol to convert the binary string to a long integer
  // The third argument '2' specifies that the string is in base 2
  long result = strtol(cstr, NULL, 2);

  // Check for any conversion errors
  if (result == 0 && cstr[0] != '0') {
    Serial.println("Error: Conversion failed. Input may not be a valid binary string.");
    return -1; // Indicate an error
  }

  return (int)result;
}