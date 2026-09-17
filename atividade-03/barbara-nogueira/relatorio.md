# Atividade 03 — Estado temporal e resiliência

## 1. Identificação

Estudante: Bárbara Nogueira. Matrícula: 202004744.
Projeto do grupo: Não dê nem água.
Responsabilidade: estado temporal e resiliência, com expiração de leituras, bloqueio da autorização e recuperação.
Execução realizada no Wokwi pelo navegador em 17/09/2026. Os resultados foram documentados por capturas do circuito e do monitor serial. Os tempos apresentados são relativos ao início da simulação.

## 2. Relação com as Atividades 01 e 02

O projeto monitora e irriga plantas domésticas. A Atividade 01 identificou sensores, usuários e dependência de conectividade. A Atividade 02 estabeleceu a necessidade de dados atuais para autorizar atuação. Este protótipo isola a validade temporal da umidade do solo.

O ESP32 mantém estado e executa a regra localmente para permitir sua observação no Wokwi. Nesse recorte, exerce funções de dispositivo e processamento de borda. Não é implementada comunicação de rede. A decisão local não modifica a arquitetura completa registrada na Atividade 02, cuja decisão está na nuvem.

## 3. Fenômeno, entrada, unidade e faixa

Um potenciômetro representa um índice fictício de umidade de solo entre 0 e 100%. A leitura ADC de 12 bits, entre 0 e 4095, é convertida por valor × 100 / 4095. Não há aquisição, calibração ou validação de umidade física real.

Uma chave representa a interrupção da produção de leituras: esquerda permite amostrar; direita pausa. A pausa não apaga o último valor. A chave não representa a desconexão elétrica real de um sensor. Sua simulação de bounce foi desabilitada para isolar o teste temporal.

Valores não finitos ou fora de [0,100] são inválidos. Digitar i no monitor serial injeta -1 como leitura inválida. Isso testa a lógica de qualidade, sem simular uma falha elétrica específica.

## 4. Circuito e componentes

ESP32 DevKit v1, um potenciômetro, uma chave deslizante, um LED verde, um LED vermelho e dois resistores de 220 ohms.

Potenciômetro: VCC em 3V3, GND em GND e SIG em GPIO34.
Chave: terminal comum 2 em GPIO23, terminal 1 em GND e terminal 3 desconectado. GPIO23 usa INPUT_PULLUP.
LED verde: GPIO18 → resistor → anodo; catodo em GND.
LED vermelho: GPIO19 → resistor → anodo; catodo em GND.

O LED verde representa autorização lógica de irrigação. Não é uma bomba nem indica água aplicada. O vermelho indica estado desconhecido, obsoleto ou inválido. Em NORMAL e AGUARDANDO, ambos ficam apagados; o estado detalhado aparece no monitor serial.

## 5. Contrato do evento

O programa produz JSON no monitor serial a 115200 baud. Tipos: umidade.leitura, estado.inicial, estado.alterado, dispositivo.status e leitura.invalida.

Campos: eventType (tipo), deviceId (esp32-barbara-01), entityId (vaso-01), eventTimeMs (ocorrência em ms desde o início), sequence (contador crescente por execução), value (último valor válido ou null), unit (pct_simulado), state, valid, actuatorAuthorized e ageMs (idade da última amostra válida ou null). leitura.invalida inclui rejectedValue=-1.

Exemplo de leitura: {"eventType":"umidade.leitura","deviceId":"esp32-barbara-01","entityId":"vaso-01","eventTimeMs":3000,"sequence":8,"value":20.00,"unit":"pct_simulado","state":"AGUARDANDO","valid":true,"actuatorAuthorized":false,"ageMs":0}.

millis() não representa UTC. eventTimeMs e sequence reiniciam em cada execução; não servem para ordenar execuções diferentes sem identidade adicional. Nos eventos de estado e status, eventTimeMs é o instante do status/transição, enquanto ageMs informa a idade da medição retida. value retido não implica dado válido: valid=false em estados de falha.

## 6. Estado, regra e atuação

Estados: DESCONHECIDO, NORMAL, AGUARDANDO, AUTORIZADO, DADO_OBSOLETO e LEITURA_INVALIDA.

Amostragem a cada 1000 ms. Solo fictício seco: valor < 30%. Igual a 30% é NORMAL. Três amostras secas válidas consecutivas autorizam a saída; com a amostragem regular, isso requer aproximadamente dois segundos entre a primeira e a terceira. Uma amostra não seca interrompe a contagem.

A leitura vence quando idade >= 5000 ms. O loop verifica a idade continuamente, mesmo sem novas amostras. Ao vencer, preserva o último valor, zera a contagem, entra em DADO_OBSOLETO, desliga o verde e liga o vermelho. A ausência inicial mantém DESCONHECIDO.

Entrada inválida bloqueia imediatamente a autorização. A recuperação, tanto de inválido quanto de obsoleto, exige novas leituras: uma leitura não seca retorna a NORMAL; três secas consecutivas retornam a AUTORIZADO. A autorização não é um pulso de bomba; mantém-se enquanto as condições forem válidas. Esse protótipo não implementa controle de volume, cooldown ou histerese da bomba, que pertencem ao recorte de decisão e atuação.

As saídas são escritas de forma idempotente; não há comandos de bomba repetidos. O contador de amostras evita autorização por um pico seco isolado. Os tempos reduzidos facilitam observar o comportamento e não equivalem aos parâmetros de cultivo da Atividade 02.

## 7. Testes e resultados no Wokwi

Os testes foram realizados com manipulação do potenciômetro e da chave durante a execução pelo navegador. As capturas registram instantes selecionados, não um log completo da sessão. Os resultados observados abaixo se limitam aos valores, estados e saídas visíveis. Tempos de simulação não correspondem necessariamente ao tempo decorrido no relógio do computador.

### 7.1 Estado normal

Estado inicial do cenário: coleta habilitada, entrada fictícia próxima de 60% e autorização desligada.

Sequência aplicada: manter o potenciômetro na posição inicial e permitir novas leituras pela chave à esquerda.

Resultado esperado: estado NORMAL, informação válida, autorização false e ambos os LEDs de indicação apagados.

Resultado observado: na captura de 17h01min00s, o evento umidade.leitura apresenta eventTimeMs=12000, sequence=25, value=60.02, state=NORMAL, valid=true, actuatorAuthorized=false e ageMs=0. O evento de status seguinte, sequence=26, confirma a mesma condição. Os LEDs de autorização e falha estão apagados; o LED de alimentação da placa não participa dessa indicação.

Explicação: 60,02% é maior que o limiar de solo seco de 30%. A medição corrente é válida, mas não satisfaz a condição para autorização.

Evidência: evidencias/teste-normal.png. Resultado compatível com o esperado.

### 7.2 Decisão e resposta observável

Estado inicial de referência: NORMAL com entrada acima do limiar, conforme o teste anterior. A mudança exata do potenciômetro e as primeiras três amostras secas não estão integralmente registradas nas capturas.

Sequência aplicada: ajustar o potenciômetro para aproximadamente 20% e manter a coleta habilitada. A regra implementada exige três amostras secas consecutivas antes de autorizar.

Resultado esperado: passar por AGUARDANDO e alcançar AUTORIZADO após três amostras secas válidas; verde aceso e vermelho apagado.

Resultado observado: na captura de 17h09min19s, uma leitura em eventTimeMs=303816, sequence=601, mostra value=20.73, state=AUTORIZADO, valid=true, actuatorAuthorized=true e ageMs=0. A leitura em 304816 ms, sequence=603, mantém a autorização. O LED verde está aceso e o vermelho apagado. A captura de 17h10min54s também mostra autorização mantida com leituras atuais de 20,73%.

Explicação: o índice fictício está abaixo de 30%, com dados válidos. A saída observável representa autorização lógica, sem bombeamento real. A persistência de três amostras é definida no código; a captura comprova o estado autorizado, mas não registra isoladamente cada amostra que levou à primeira autorização.

Evidência: evidencias/teste-decisao.png. A resposta final está compatível com o esperado. A etapa AGUARDANDO também é observada no teste de recuperação descrito abaixo.

### 7.3 Teste adversarial individual — matrícula final 4

Situação obrigatória: informação que continua armazenada depois de perder a validade.

Estado inicial: AUTORIZADO, valor de 20,73% e coleta inicialmente ativa.

Sequência aplicada: interromper novas amostras pela chave, sem alterar a entrada fictícia, e acompanhar a idade do último dado. A captura de 17h09min48s mostra o estado autorizado ainda preservado durante a tolerância temporal.

Resultado esperado: manter o valor na memória, mas retirar a autorização ao completar 5000 ms desde a última amostra válida, sinalizando DADO_OBSOLETO e acendendo o vermelho.

Resultado observado: em eventTimeMs=323000, sequence=636, o status mostra value=20.73, state=AUTORIZADO, valid=true, actuatorAuthorized=true e ageMs=4184. Em eventTimeMs=323816, sequence=637, aparece estado.alterado com state=DADO_OBSOLETO, valid=false, actuatorAuthorized=false e ageMs=5000. A linha de diagnóstico registra reason=validade_expirada e authorization=OFF. O valor permanece 20,73%. No status de 324000 ms, sequence=638, a idade é 5184 ms e o bloqueio permanece. A imagem mostra verde apagado e vermelho aceso.

Pelo par tempo/idade, o instante da última leitura válida pode ser deduzido como 318816 ms: 323816 − 5000. A captura anterior contém uma leitura nesse instante. Portanto, a expiração registrada é consistente com o limite configurado de cinco segundos.

Explicação: uma implementação ingênua poderia continuar usando 20,73% como condição presente indefinidamente. O protótipo separa o valor armazenado da sua validade: a verificação temporal roda mesmo sem novas amostras, expira o estado e bloqueia a resposta.

Evidências: evidencias/teste-adversarial.png e evidencias/adversarial-antes-expiracao.png. Resultado compatível com o esperado.

### 7.4 Recuperação após obsolescência

Estado inicial: DADO_OBSOLETO com o valor antigo de 20,73% retido.

Sequência aplicada: reabilitar a coleta mantendo a entrada próxima de 20%.

Resultado esperado: reiniciar a contagem de amostras, passar por AGUARDANDO e retornar a AUTORIZADO após três novas amostras secas consecutivas.

Resultado observado: a captura de 17h12min19s contém status obsoleto em 403000 ms, seguido de umidade.leitura em 403830 ms, sequence=745, com value=20.73, state=AGUARDANDO, valid=true, actuatorAuthorized=false e ageMs=0. A leitura em 404830 ms, sequence=748, ainda registra AGUARDANDO. A captura de 17h12min25s mostra leituras em 409830, 410830 e 411830 ms com AUTORIZADO e LED verde aceso.

A janela do monitor serial na captura de recuperação exibe mensagens anteriores ao estado atual dos LEDs. Por isso, a análise temporal usa os instantes de cada evento. O momento exato da terceira amostra de recuperação não está visível; as imagens comprovam a passagem por AGUARDANDO e o posterior retorno a AUTORIZADO.

Evidências: evidencias/teste-recuperacao.png e evidencias/recuperacao-autorizada.png. As etapas visíveis são compatíveis com a regra.

### 7.5 Qualidade e limites da evidência

O comando i injeta uma leitura inválida, e seu bloqueio é coberto pelos testes locais. Não há captura desse cenário no Wokwi entre as evidências apresentadas; ele não é declarado como teste executado no simulador. O adversarial obrigatório deste estudante é o de expiração, documentado acima.

## 8. Verificação local realizada

A lógica real de controle foi compilada com g++ e testada por asserções. Foram verificados NORMAL, três amostras secas, idade 4999 ms, expiração exatamente em 5000 ms, retenção de valor antigo, recuperação, valores inválidos, NaN, igualdade ao limiar e passagem do contador de tempo por rollover.

O sketch completo também foi compilado e executado em um harness C++ com interfaces Arduino substituídas. Foram verificadas as saídas digitais e analisados os eventos JSON. Logs estão em evidencias/verificacao-local-controle.txt e evidencias/verificacao-local-firmware.txt. Isso comprova a lógica nos cenários locais, mas não comprova compilação para ESP32, conexões do circuito ou execução Wokwi.

## 9. Limitações

Não são validados umidade física, precisão, calibração, ruído real, instalação, dinâmica de secagem, fluxo de água, segurança elétrica, consumo ou autonomia. Não há nuvem, tomada comercial, Alexa ou aplicativo implementados. O LED indica uma decisão lógica, sem realimentação física. A expiração depende de o processador continuar executando; um travamento real exigiria outras medidas. O estado em RAM reinicia como desconhecido após reboot.

## 10. Uso de IA generativa

Ferramenta: OpenAI/Codex. Uso: proposta de divisão dos recortes, estrutura do circuito, elaboração do código, testes locais e redação do relatório a partir das evidências de simulação.

Síntese das orientações: desenvolver um protótipo de plantas domésticas relacionado às atividades anteriores, especializado em expiração de dados e no adversarial de matrícula final 4.

Sugestões adotadas: entrada substituta declarada, chave para interromper amostras, estados explícitos, temporização não bloqueante e eventos estruturados. Adaptação: a saída foi definida como autorização lógica, com regra local restrita ao recorte da simulação.

Erro identificado e corrigido: a primeira versão do circuito utilizava nomes numéricos para quatro terminais da placa, omitindo o prefixo D exigido pelo componente ESP32 DevKit v1 no Wokwi. Foram corrigidos para D34, D23, D18 e D19. Os números de GPIO no programa permaneceram 34, 23, 18 e 19.

Limitação identificada: os testes locais não validam a execução Wokwi; resultados de simulação foram documentados separadamente com capturas reais. As imagens não contêm o histórico completo de todas as transições. A estudante permanece responsável por compreender, revisar e explicar o material entregue.

## 11. Link compartilhável e conclusão

Link compartilhável: https://wokwi.com/projects/475420562350777345

As capturas documentam estado normal, autorização e expiração de dado armazenado, com saída visual e eventos estruturados. A recuperação também está registrada. A evidência adversarial demonstra retirada da autorização exatamente em ageMs=5000, preservando o valor antigo. O protótipo valida esse comportamento lógico no simulador, sem demonstrar irrigação física ou calibração de umidade real.

## Referências

Enunciado da Atividade 03 e materiais das aulas 1 a 4.
https://docs.wokwi.com/guides/esp32
https://docs.wokwi.com/diagram-format
https://docs.wokwi.com/parts/wokwi-potentiometer
https://docs.wokwi.com/parts/wokwi-slide-switch
