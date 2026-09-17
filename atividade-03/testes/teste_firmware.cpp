#include "Arduino.h"
#include <cassert>
uint32_t relogio=0;
int chave=LOW, analogico=2457, saidas[40]={};
SerialLocal Serial;
#include "../barbara-nogueira/sketch.ino"
int main() {
 setup();
 for(relogio=0; relogio<=2000; relogio+=10) loop();
 assert(saidas[18]==LOW && saidas[19]==LOW);
 analogico=819;
 for(;relogio<=5000;relogio+=10) loop();
 assert(saidas[18]==HIGH);
 chave=HIGH;
 for(;relogio<10000;relogio+=10) loop();
 assert(saidas[18]==HIGH);
 loop(); assert(saidas[18]==LOW && saidas[19]==HIGH);
 assert(controle.ultimoValor>19 && controle.ultimoValor<21);
 chave=LOW;
 for(;relogio<=12000;relogio+=10) loop();
 assert(saidas[18]==HIGH && saidas[19]==LOW);
}
