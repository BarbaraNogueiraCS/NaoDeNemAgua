#include "../barbara-nogueira/controle.h"
#include <cassert>
#include <iostream>
int main() {
 Controle c; assert(!c.autorizado());
 c.receber(60,1000); c.atualizar(2000); assert(c.estado==Controle::NORMAL);
 std::cout << "NORMAL: entrada 60%, autorizacao OFF\n";
 c.receber(20,3000); assert(!c.autorizado());
 c.receber(20,4000); assert(!c.autorizado());
 c.receber(20,5000); assert(c.autorizado());
 std::cout << "DECISAO: tres amostras secas, autorizacao ON\n";
 c.atualizar(9999); assert(c.autorizado());
 c.atualizar(10000); assert(c.estado==Controle::DADO_OBSOLETO);
 assert(!c.autorizado() && c.ultimoValor==20 && c.ultimaLeituraMs==5000);
 std::cout << "ADVERSARIAL FINAL 4: valor 20% retido; idade 5000ms; DADO_OBSOLETO; autorizacao OFF\n";
 c.receber(20,11000); assert(!c.autorizado());
 c.receber(20,12000); c.receber(20,13000); assert(c.autorizado());
 c.receber(-1,14000); assert(c.estado==Controle::LEITURA_INVALIDA && !c.autorizado());
 c.receber(30,15000); assert(c.estado==Controle::NORMAL);
 c.receber(NAN,16000); assert(c.estado==Controle::LEITURA_INVALIDA);
 Controle wrap; wrap.receber(20,0xfffff000u); wrap.receber(20,0xfffff100u);
 wrap.receber(20,0xfffff200u); wrap.atualizar(uint32_t(0xfffff200u+5000u));
 assert(wrap.estado==Controle::DADO_OBSOLETO);
 std::cout << "LIMITES: recuperacao, invalidos, limiar e rollover aprovados\n";
}
