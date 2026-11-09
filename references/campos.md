# Campos da cotação residencial

Regras tiradas de cotações reais da corretora (HDI, Tokio Marine, Allianz e Zurich) e das orientações do gerente comercial. Em outras seguradoras os nomes mudam, mas a informação é a mesma. A seção "Por seguradora", no fim, mostra onde cada coisa fica.

## Formato do JSON

```json
{
  "seguradora": "HDI",
  "segurado": "MARIA APARECIDA DOS SANTOS",
  "local_risco": "RUA DAS FLORES, 123 – CENTRO – ANDRADINA/SP",
  "coberturas": [
    {"nome": "Incendio", "lmi": "350.000,00", "pos": "10%", "minimo": "350,00"},
    {"nome": "Responsabilidade Civil Familiar", "lmi": "10.000,00"},
    {"nome": "Danos Eletricos", "lmi": "10.000,00", "pos": "10%", "minimo": "600,00"},
    {"nome": "Perda ou Pagto. de Aluguel a Terceiros", "lmi": "12.000,00"},
    {"nome": "Vendaval", "lmi": "20.000,00", "pos": "10%", "minimo": "550,00"}
  ],
  "pagamento": [
    {"parcelas": "A Vista", "valor": "192,08", "descricao": ""},
    {"parcelas": "06x", "valor": "32,01", "descricao": "Cartão de Crédito / Débito / Carnê"}
  ]
}
```

Use os valores como texto, no formato brasileiro (`350.000,00`), exatamente como aparecem na cotação. O script põe o `R$` e os dois-pontos depois do nome da cobertura.

## Segurado e local de risco

| Campo | Regra |
|---|---|
| `segurado` | Nome do segurado/proponente, em maiúsculas. |
| `local_risco` | Endereço **do imóvel segurado** (seção "Local em risco", "Local de risco", "Endereço do risco"), **não** o de cobrança. Formato: `RUA NOME, NÚMERO – COMPLEMENTO – BAIRRO – CIDADE/UF`, em maiúsculas, separado por ` – `. Escreva o logradouro por extenso (`R` → `RUA`, `AV` → `AVENIDA`). Inclua o complemento quando houver, abreviando apartamento como `AP` (`APTO 17`, `apt 802` → `AP 17`, `AP 802`; `casa 6` → `CASA 6`). Omita o CEP. Se o endereço de cobrança for diferente do local de risco, use o de risco e avise o usuário. O script já escreve "LOCAL DE RISCO: – " antes (o travessão é do modelo da corretora). |

## Coberturas

- Inclua **toda cobertura contratada que tenha valor (LMI)**, na ordem em que a seguradora lista. Coberturas oferecidas mas não contratadas (sem LMI, "Não contratada") ficam de fora.
- Ficam de fora também os itens sem LMI: planos de assistência 24h, "Cláusula Específica de Valor Novo", "Coberturas de Assistências Essenciais", serviços PET. Cite-os no resumo ao usuário.
- `nome`: copie o nome **como a seguradora escreve**, com as mesmas abreviações e acentos (`Incendio`, `Incend / Raio / Expl / Fumaça / Q.Aero`, `Vendaval/granizo`). Não traduza nem padronize. Corrija só erro de digitação evidente.
- `lmi`: o Limite Máximo de Indenização, sem `R$`.

## Franquias (POS)

Cada cobertura pode ter a sua. Procure na seção de franquias ou participação obrigatória (às vezes fica numa coluna da própria tabela de coberturas).

- `pos`: o percentual sobre os prejuízos, como `10%` (sem casas decimais: "10.00%" vira `10%`).
- `minimo`: o valor mínimo da franquia, sem `R$` (`350,00`).
- "Sem franquia", "Sem Franquia" ou cobertura que não aparece na lista de franquias: deixe `pos` e `minimo` de fora (a célula fica em branco).
- Franquia que só vale para parte da cobertura (HDI: incêndio "com mínimo de R$ 350,00 para Queda de Raio") entra na linha da cobertura normalmente: `10%` e `350,00`.
- Franquia de valor fixo, sem percentual: deixe `pos` de fora e ponha o valor em `minimo`.
- Franquia de cobertura que não foi contratada (Allianz lista "Desmoronamento" e "Jóias" com franquia, mas sem LMI): ignore.

## Opções de pagamento

**Regra do gerente comercial: sempre o máximo de parcelas sem juros, em todas as modalidades.**

**Linha 1 – `A Vista`:** o preço total em 1x (escreva `A Vista`, sem acento, como no modelo).

**Demais linhas:** para cada forma de pagamento (cartão de crédito, débito em conta, carnê/boleto/ficha), ache **o maior número de parcelas ainda sem juros**. Monte uma linha para cada um desses máximos, do menor para o maior. A descrição lista todas as formas que aceitam aquele número sem juros:

- HDI: débito e carnê sem juros até 6x, cartão até 9x → `06x 32,01 Cartão de Crédito / Débito / Carnê` e `09x 21,34 Cartão de Crédito`
- Tokio: carnê ("Ficha") até 4x, cartão e débito até 12x → `04x 34,22 Cartão de Crédito / Débito / Carnê` e `12x 11,41 Cartão de Crédito / Débito`
- Zurich: boleto até 6x, débito até 10x, cartão até 12x → `06x Cartão de Crédito / Débito / Carnê`, `10x Cartão de Crédito / Débito`, `12x Cartão de Crédito`
- Allianz: só cartão, até 12x → `12x 12,92 Cartão de Crédito`

Detalhes:
- Ordem dos nomes: `Cartão de Crédito / Débito / Carnê`. "Boleto", "Ficha" e "Carnê" entram como `Carnê`; "Débito em conta", "Deb. C/C" e "Débito/PIX" entram como `Débito`.
- Se a tabela não disser se tem juros, considere **sem juros** a parcela em que *número de parcelas × valor* fica a no máximo 1 centavo por parcela do preço à vista (10x pode diferir até R$ 0,10, por arredondamento). Com juros, a diferença é de reais, não de centavos.
- Ignore a forma ou o número de parcelas que a seguradora deixou "selecionado" na cotação (Allianz: "Modo de Pagamento: Cartão de Crédito, 6 parcelas"). A regra é sempre o máximo sem juros.
- "1 + N" quer dizer N+1 parcelas (`1+5` = `06x`). Na Zurich, "0+N" (1ª a 30 dias) quer dizer N parcelas.
- Se a mesma forma tiver duas variantes (Zurich: boleto com 1ª à vista e boleto com 1ª a 30 dias), use a que der **mais** parcelas sem juros.
- Se a mesma quantidade tiver valores diferentes entre as formas (centavos de arredondamento), use o valor da primeira forma listada na descrição.
- Parcelas com dois dígitos e "x" (`04x`, `12x`). Uma forma cujo máximo sem juros é 1x não gera linha.

## Por seguradora

**HDI ("HDI EM CASA", ~5 páginas)**
- Local de risco: bloco "LOCAL EM RISCO" (Endereço, Nro, Complemento, Bairro, Cidade, UF). Compare com "End. Cobrança".
- Coberturas: "COBERTURAS CONTRATADAS". Ignore "Clausula Especifica de Valor Novo" e "Coberturas de Assistencias Essenciais".
- Franquias: "PARTICIPAÇÃO OBRIGATÓRIA" ("10.00% sobre os prejuízos indenizáveis com mínimo de R$ 600,00").
- Pagamento: "Opções de Pagamento", sem indicar juros (use a conta parcelas × valor). **O texto extraído embaralha o cabeçalho: renderize a página como imagem.** A ordem real das 6 colunas de valores é: **Cartão de Crédito** | Débito (1ª no Ato) | Débito (1ª a 30 dias) | Débito (Melhor Data) | Carnê (1ª no Ato) | Carnê (1ª a 7 dias). Colunas com "-" não estão disponíveis. Em geral o cartão vai além de 6x sem juros (9x ou 10x), e débito e carnê param em 6x.
- Validade: "Esta cotação tem validade de 30 dia(s), até DD/MM/AAAA".

**Tokio Marine ("Residencial Premiado", ~4 páginas)**
- Local de risco: "Local de Risco / Número / Complemento / Bairro / Cidade / Estado" (vem como `R DAS FLORES`: escreva `RUA DAS FLORES`).
- Coberturas: tabela com **três planos de assistência** (Básico, Especial, VIP). O LMI das coberturas é o mesmo nos três; muda só o preço. **O plano escolhido é o que vem destacado** ("O cálculo destacado será usado para parcelamento"). O texto extraído não mostra o destaque: renderize a página 1 como imagem e veja qual coluna está destacada. Se não der para saber, use o Básico e avise.
- Franquias: tabela "Cobertura | P.O.S" (em geral só vendaval).
- Pagamento: tabelas "Cartão", "Débito/PIX Automático" e "Ficha" (= Carnê), com "Sem juros" indicado, uma coluna por plano. Use a coluna do plano escolhido.
- Validade: "Validade cotação" no topo.

**Allianz ("Residência", ~5 páginas)**
- Local de risco: "Endereço do local segurado" (página 4), que vem como `RUA Rua das Flores, 123 -  - BAIRRO - CEP - CIDADE/UF`: limpe a repetição, os traços vazios e o CEP.
- Coberturas: "Preço por Cobertura". Linhas sem LMI (Desmoronamento, Jóias, Roubo fora do local) não foram contratadas. "Assistência 24h ESSENCIAL" fica de fora.
- Franquias: "PARTICIPAÇÃO OBRIGATÓRIA (FRANQUIA)" ("10% dos prejuízos com mínimo de R$ 700,00").
- Pagamento: só a tabela de cartão ("DEMAIS OPÇÕES DE PARCELAMENTO NO CARTÃO"), sem indicar juros (use a conta parcelas × valor).
- Validade: "Garantimos esta cotação até DD/MM/AAAA".

**Zurich ("Zurich Residência", ~5 páginas)**
- Local de risco: "Endereço do Risco / Número / Complemento / Bairro / Cidade / UF" (vem em maiúsculas e minúsculas: passe para maiúsculas).
- Coberturas e franquias: na mesma tabela ("Franquia: 10 % prej. ind. Min R$ 500,00" ou "Sem Franquia"). "Assistência Completa +" fica de fora. Coberturas com prêmio 0,00 mas com LMI (contenção e salvamento, custo de defesa) **entram**.
- Pagamento: "Parcelamento do Prêmio", uma linha por plano: "1+N sem juros (Cartão de Crédito)", "1+N(1ª a vista 7 dia-Deb.C/C)", "1+N(1ª a vista 5 dia-Boleto)", "0+N(1º à 30 Dias-...)". Juros na última coluna (0,00 % = sem juros).
- Validade: coluna "Validade" no topo.
