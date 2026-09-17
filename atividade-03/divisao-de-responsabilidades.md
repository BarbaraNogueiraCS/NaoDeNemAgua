# Atividade 03 — Divisão de responsabilidades

Projeto: **Não dê nem água**. Cada integrante desenvolve, testa e entrega um protótipo individual.

| Integrante | Responsabilidade | Recorte |
|---|---|---|
| Matheus Vieira Mendes Pacheco | Sensoriamento e qualidade | Umidade fictícia, validação, filtragem e indicação de falhas. |
| Davi Duarte Neco | Decisão e atuação | Persistência de solo seco, histerese, pulso limitado e cooldown da bomba simulada. |
| Bárbara Nogueira — 202004744 | Estado temporal e resiliência | Expiração de leituras, bloqueio de autorização com dados obsoletos e recuperação. |

Todos os recortes incluem ESP32, entrada simulada, validação, evento JSON, estado, regra e saída observável. As implementações devem apresentar diferenças verificáveis. Cada integrante executa os três testes e entrega seu próprio ZIP no SIGAA. Os testes adversariais de Matheus e Davi dependem do final de suas matrículas.

No recorte de Bárbara, o teste adversarial obrigatório (final 4) verifica informação que permanece armazenada após perder a validade.
