---
name: orcamento-residencial
description: Gera a cotação de seguro RESIDENCIAL de 1 página da S.R. Martins Corretora de Seguros (logo, cabeçalho, tabela de coberturas com franquias e opções de pagamento) a partir da cotação da seguradora (HDI, Tokio Marine, Allianz, Zurich, Porto, Mapfre, Bradesco, Liberty/Yelum etc.). Use sempre que o usuário mandar uma cotação de seguro residencial, de casa ou de apartamento e pedir o orçamento, o "PDF de 1 página", a "cotação pro cliente" ou a "versão da SR Martins", mesmo sem falar "skill". Também é chamada pelos comandos /orcamento-residencial e /orçamento-residencial junto com o PDF. Para seguro de automóvel ou moto, use a skill orcamento.
---

# Cotação de seguro residencial – S.R. Martins

A seguradora manda uma cotação longa, com textos legais, planos de assistência e tabelas de parcelamento. Para o cliente, a corretora manda **1 página** com o essencial: segurado, local de risco, cada cobertura contratada com seu valor e sua franquia, e as opções de pagamento.

O seguro residencial tem uma diferença importante em relação ao de automóvel: **cada cobertura (verba) tem a sua franquia, e cada seguradora tem franquias diferentes**. Uma cobra franquia em danos elétricos, outra em roubo, outra não. O cliente precisa ver isso com clareza, porque é o que ele vai pagar do bolso num sinistro.

O trabalho se divide em duas partes:
- **Você (Claude)** lê a cotação e decide o conteúdo de cada campo. Cada seguradora escreve de um jeito.
- **O script** desenha o PDF no layout oficial, sempre igual.

Quando o usuário mandar só o comando (/orcamento-residencial) e o PDF, não pergunte nada antes: faça o passo a passo e devolva a cotação pronta. Pergunte só o que faltar de verdade.

## Passo a passo

Para rodar os scripts, use `<skill>/.venv/bin/python` se essa pasta existir (é a instalação local, já com PyMuPDF). Se não existir, use `python`.

1. **Ler a cotação:**
   ```bash
   python <skill>/scripts/extrair_texto.py "<cotacao.pdf>"
   ```
   Se der `No module named 'fitz'`, instale com `pip install pymupdf` (se o ambiente permitir). Páginas sem texto (escaneadas) são salvas como imagem e o caminho aparece na saída: abra e leia com atenção.

2. **Montar o JSON de dados** seguindo `references/campos.md`. Leia esse arquivo toda vez: ele traz as regras de coberturas, franquias e pagamento e as particularidades de cada seguradora.

3. **Gerar o PDF:**
   ```bash
   python <skill>/scripts/gerar_orcamento.py dados.json "<NOME DO SEGURADO>.pdf"
   ```
   O nome do arquivo é o nome completo do segurado em maiúsculas. Salve na mesma pasta da cotação, a menos que o usuário peça outra. Se já existir um arquivo com esse nome (muitas vezes é a cotação que a corretora fez à mão), o script se recusa a gravar: pergunte se pode substituir (`--sobrescrever`) ou use outro nome, como `NOME (gerado).pdf`.

4. **Conferir a página.** Renderize e olhe se nada ficou cortado ou fora do lugar:
   ```bash
   python -c "import fitz,sys; fitz.open(sys.argv[1])[0].get_pixmap(dpi=90).save(sys.argv[2])" saida.pdf previa.png
   ```

5. **Responder ao usuário** com o caminho do PDF e um resumo: segurado, local de risco, coberturas com franquia e opções de pagamento. Depois, numa seção **"Pontos de atenção"**, liste tudo o que a verificação abaixo encontrou.

## Pontos de atenção (o que apontar ao usuário)

O gerente comercial pediu que o Claude aponte qualquer coisa suspeita. Antes de responder, confira e avise sobre:

- **Validade:** cotação vencida ou que vence em até 2 dias.
- **Vigência já começou:** em renovação, se o início da vigência já passou, avise que pode haver dias sem cobertura até a renovação ser fechada.
- **Endereço:** o local de risco é o endereço do imóvel segurado, não o de cobrança. Se os dois forem diferentes (outro bairro, outro número, complemento faltando), avise.
- **Franquias que pesam:** franquia mínima alta perto do valor da cobertura (ex.: mínimo de R$ 600,00 numa cobertura de R$ 5.000,00), franquia em roubo ou em danos elétricos, ou percentual acima de 10%.
- **Prêmio desproporcional:** uma cobertura com prêmio muito alto para o valor (ex.: R$ 423,64 de prêmio para R$ 10.000,00 de danos elétricos, metade do seguro inteiro).
- **Coberturas comuns que faltam:** sem danos elétricos, sem roubo, sem RC familiar, sem vendaval. O cliente pode achar que tem.
- **Tipo de verba:** cotação só de "Prédio" (não cobre o conteúdo) ou "Prédio e Conteúdo". Se for só prédio e tiver cobertura de roubo de bens, ou o contrário, avise.
- **Coberturas sem valor:** cláusulas e assistências que aparecem na cotação mas não entram na tabela (assistência 24h, cláusula de valor novo). Cite numa linha, para o usuário saber.
- **Mais de um plano** (Tokio: Básico, Especial e VIP): diga qual plano você usou e por quê.
- **Valor estranho:** LMI que parece digitado errado (um zero a mais ou a menos), coberturas repetidas, totais que não fecham.

Não deixe de gerar a cotação por causa desses pontos. Gere e avise.

## Quando a cotação foge do padrão

- **Seguro de automóvel ou moto:** use a skill `orcamento`.
- **Mais de um local de risco** na mesma cotação: gere uma página por local e avise.
- **Seguro empresarial ou condomínio:** este modelo é residencial. Diga ao usuário em vez de forçar os campos.
