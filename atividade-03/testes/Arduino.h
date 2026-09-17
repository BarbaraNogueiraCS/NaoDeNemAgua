#pragma once
#include <stdint.h>
#include <cstdarg>
#include <cstdio>
#define INPUT 0
#define INPUT_PULLUP 2
#define OUTPUT 1
#define HIGH 1
#define LOW 0
extern uint32_t relogio;
extern int chave;
extern int analogico;
extern int saidas[40];
inline uint32_t millis() { return relogio; }
inline void pinMode(int,int) {}
inline void analogReadResolution(int) {}
inline void digitalWrite(int pin,int value) { saidas[pin]=value; }
inline int digitalRead(int) { return chave; }
inline int analogRead(int) { return analogico; }
struct SerialLocal {
 void begin(int) {}
 int available() { return 0; }
 int read() { return -1; }
 void print(const char* s) { std::printf("%s",s); }
 void print(unsigned long n) { std::printf("%lu",n); }
 void println(const char* s) { std::printf("%s\n",s); }
 void printf(const char* f, ...) { va_list a; va_start(a,f); std::vprintf(f,a); va_end(a); }
};
extern SerialLocal Serial;
