# Atividade 03 — Protótipos individuais

Projeto: **Não dê nem água**.

A divisão está em [divisao-de-responsabilidades.md](divisao-de-responsabilidades.md). O protótipo de Bárbara Nogueira (202004744) está em [barbara-nogueira/](barbara-nogueira/).

## Executar o protótipo de Bárbara

1. Abrir https://wokwi.com/projects/new/esp32 e salvar um projeto na conta individual.
2. Substituir `sketch.ino` e `diagram.json` pelos arquivos da pasta `barbara-nogueira/`.
3. Adicionar um arquivo `controle.h` no editor e copiar seu conteúdo. Ele é uma dependência obrigatória do sketch e deve integrar o ZIP. Não há bibliotecas adicionais.
4. Iniciar a simulação. Chave esquerda coleta; direita interrompe. Potenciômetro ajusta umidade fictícia. Verde indica autorização e vermelho indica falha/obsolescência. O monitor serial explica os estados e mostra JSON.
5. Executar os três testes descritos em `relatorio.md` e salvar capturas na pasta `evidencias/`.
6. Inserir o link compartilhável e os resultados observados no relatório, gerar novamente `relatorio.pdf` e montar a entrega individual.

## Estado de validação

A lógica e o sketch foram compilados e testados localmente com g++, usando interfaces Arduino substituídas no segundo teste. Os logs são identificados como verificações locais. Execução Wokwi, compilação para ESP32, três capturas e link público estão pendentes. O relatório PDF preparatório explicita essas pendências. Não há capturas simuladas ou resultados Wokwi inventados.

## Verificação local reproduzível

```bash
g++ -std=c++11 -Wall -Wextra -Werror atividade-03/testes/teste_controle.cpp -o /tmp/teste-controle
/tmp/teste-controle
g++ -std=c++11 -Wall -Wextra -Werror -I atividade-03/testes atividade-03/testes/teste_firmware.cpp -o /tmp/teste-firmware
/tmp/teste-firmware
python3 atividade-03/gerar_relatorio.py
```

`gerar_relatorio.py` utiliza ReportLab. O PDF acompanha o estado atual de `relatorio.md`.

## Entrega

O ZIP final `atividade-03-barbara-nogueira-202004744.zip` deverá conter `sketch.ino`, `controle.h`, `diagram.json`, `relatorio.pdf` atualizado e as três capturas obrigatórias. Após completar as evidências e atualizar o relatório, executar `python3 atividade-03/montar_entrega.py`. O script verifica as pendências e monta o ZIP. A entrega individual ocorre no SIGAA. Os arquivos de testes locais podem permanecer no repositório, sem integrar o ZIP oficial.

## Referências técnicas

- [ESP32 no Wokwi](https://docs.wokwi.com/guides/esp32).
- [Formato de diagram.json](https://docs.wokwi.com/diagram-format).
- [Potenciômetro](https://docs.wokwi.com/parts/wokwi-potentiometer).
- [Chave deslizante](https://docs.wokwi.com/parts/wokwi-slide-switch).
