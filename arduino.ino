#include <LedControl.h>

int DIN = 11;
int CS =  12;
int CLK = 13;
LedControl lc=LedControl(DIN,CLK,CS,0);
char value = 'f';

void setup(){
 lc.shutdown(0,false);  
 lc.setIntensity(0,3);
 lc.clearDisplay(0);
 pinMode(4, INPUT);
 Serial.begin(9600);
}

void loop(){ 

    byte zero[8]=   {0x3C,0x66,0x42,0x42,0x42,0x42,0x66,0x3C};
    byte un[8]=     {0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18};
    byte t[8]=      {0x7E,0x7E,0x18,0x18,0x18,0x18,0x18,0x18};
    byte h[8]=      {0x66,0x66,0x66,0x7E,0x7E,0x66,0x66,0x66};
    byte e[8]=      {0x7E,0x7E,0x60,0x7C,0x7C,0x60,0x7E,0x7E};
    byte m[8]=      {0xC3,0xE7,0xFF,0xDB,0xC3,0xC3,0xC3,0xC3};
    byte a[8]=      {0x7E,0x7E,0x66,0x66,0x7E,0x7E,0x66,0x66};
    byte z[8]=      {0x7E,0x7E,0x06,0x1E,0x78,0x60,0x7E,0x7E};
    byte up[8]=     {0x18,0x3C,0x7E,0xDB,0x18,0x18,0x18,0x18};
    byte down[8]=   {0x18,0x18,0x18,0x18,0xDB,0x7E,0x3C,0x18};
    byte left[8]=   {0x10,0x30,0x60,0xFF,0xFF,0x60,0x30,0x10};
    byte righty[8]= {0x08,0x0C,0x06,0xFF,0xFF,0x06,0x0C,0x08};
    byte gg[8]=     {0x00,0x66,0x88,0x88,0xBB,0x99,0x66,0x00};
    byte boom[8]=   {0x00,0x00,0xA5,0x42,0xA5,0x00,0x3C,0x00};
     if(Serial.available() > 0)
  {
     value = Serial.read();
        if(value == 'd')
    {
       lc.clearDisplay(0);
       printByte(down);
    }
      else if(value == 'u')
    {
        lc.clearDisplay(0);
        printByte(up);
    }
      else if(value == 'l')
    {
        lc.clearDisplay(0);
        printByte(left);
    }
      else if(value == 'r')
    {        
        lc.clearDisplay(0);
        printByte(righty);
    } 
      else if(value == 'g')
    {        
        lc.clearDisplay(0);
        printByte(gg);
        delay(100);
    } 
      else if(value == 'o')
    {
      lc.clearDisplay(0);
      printByte(boom);  
    }
      else if(value == '0')
    {        
        lc.clearDisplay(0);
    }
      else if(value == 'x')
    {        
        printByte(righty);
        delay(500);
        printByte(boom);
        delay(100);
        printByte(down);
        delay(200);
        printByte(left);
        delay(500);
        printByte(up);
        delay(100);
        printByte(boom);
        delay(100);
    }
  }
}

void printByte(byte character [])
{
  int i = 0;
  for(i=0;i<8;i++)
  {
    lc.setRow(0,i,character[i]);
  }
}
