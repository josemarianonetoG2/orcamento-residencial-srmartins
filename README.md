# Cotação de Seguro Residencial – S.R. Martins

Skill para o Claude que transforma a cotação de seguro **residencial** da seguradora (HDI, Tokio Marine, Allianz, Zurich e outras) na **cotação de 1 página da S.R. Martins**, com logo, cabeçalho, tabela de coberturas com as franquias de cada verba e opções de pagamento, pronta para enviar ao cliente.

Para seguro de automóvel, use a skill [orcamento](https://github.com/josemarianonetoG2/orcamento-srmartins).

## Como usar

Anexe o PDF da cotação e escreva:

```
/orcamento-residencial
```

O Claude:
- lê a cotação e gera o PDF com o nome do segurado (ex.: `MARIA APARECIDA DOS SANTOS.pdf`) na mesma pasta da cotação;
- lista todas as coberturas contratadas com a franquia de cada uma (% do prejuízo e valor mínimo);
- mostra as opções de pagamento sempre com o **máximo de parcelas sem juros** em cada modalidade (cartão, débito, carnê);
- aponta o que merece atenção: cotação vencida, vigência já iniciada, endereço divergente, franquias altas, prêmio desproporcional, coberturas comuns que faltam, seguro só de prédio.

## Instalação

### No Claude (app ou claude.ai)

1. Baixe o arquivo **`orcamento-residencial.skill`** na [página de downloads](https://github.com/josemarianonetoG2/orcamento-residencial-srmartins/releases/latest).
2. No Claude, abra as configurações de **Skills** e carregue o arquivo.

### No Claude Code (Mac)

Abra o Terminal e rode:

```bash
git clone https://github.com/josemarianonetoG2/orcamento-residencial-srmartins.git ~/.claude/skills/orcamento-residencial && python3 -m venv ~/.claude/skills/orcamento-residencial/.venv && ~/.claude/skills/orcamento-residencial/.venv/bin/pip install pymupdf
```

Depois abra uma sessão nova do Claude Code e use `/orcamento-residencial`.

Para atualizar depois:

```bash
git -C ~/.claude/skills/orcamento-residencial pull
```

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `SKILL.md` | Instruções que o Claude segue, incluindo o que apontar como suspeito. |
| `references/campos.md` | Regras de coberturas, franquias e pagamento, e onde fica cada informação em cada seguradora. |
| `scripts/extrair_texto.py` | Lê o texto da cotação (e transforma páginas escaneadas em imagem). |
| `scripts/gerar_orcamento.py` | Desenha o PDF de 1 página em cima do modelo. |
| `assets/modelo_base.pdf` | Cabeçalho oficial da S.R. Martins (logo, endereço, CNPJ). |
| `assets/fonts/` | Fonte Carlito, compatível com a Calibri do modelo (licença OFL). |
