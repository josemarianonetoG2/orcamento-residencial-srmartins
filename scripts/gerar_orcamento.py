#!/usr/bin/env python3
"""Gera a cotação de seguro residencial de 1 página da S.R. Martins.

Uso:
    python gerar_orcamento.py dados.json saida.pdf [--sobrescrever]

O cabeçalho (logo, endereço, CNPJ) vem pronto de assets/modelo_base.pdf.
Este script desenha o resto (segurado, local de risco, tabela de coberturas
e opções de pagamento) nas mesmas posições do modelo em Word.
Veja o formato do JSON em references/campos.md.
"""
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "modelo_base.pdf"
FONTS = ROOT / "assets" / "fonts"

# Carlito tem as mesmas medidas da Calibri usada no modelo original.
FONT_FILES = {"reg": "Carlito-Regular.ttf", "bold": "Carlito-Bold.ttf"}

AZUL_ESCURO = (0.776, 0.851, 0.945)
AZUL_CLARO = (0.859, 0.898, 0.945)

LEFT = 42.6
RIGHT = 562.0

# Colunas da tabela (x0, x1) no modelo.
COL_COBERTURA = (28.1, 311.7)
COL_VALOR = (311.7, 425.3)
COL_POS = (425.4, 481.9)
COL_MINIMO = (481.9, 567.1)
CAB_TOPO, CAB_MEIO, CAB_BASE = 351.5, 368.1, 398.0
ALTURA_LINHA = 16.42


class Pagina:
    def __init__(self, page):
        self.page = page
        self.fonts = {}
        for key, name in FONT_FILES.items():
            path = str(FONTS / name)
            page.insert_font(fontname=key, fontfile=path)
            self.fonts[key] = fitz.Font(fontfile=path)

    def largura(self, texto, fonte, tamanho):
        return self.fonts[fonte].text_length(texto, fontsize=tamanho)

    def texto(self, x, y, texto, fonte="reg", tamanho=11, alinhar="esq", max_w=None):
        """Escreve uma linha com baseline em y. Reduz a fonte se passar de max_w."""
        if max_w is not None:
            while tamanho > 7 and self.largura(texto, fonte, tamanho) > max_w:
                tamanho -= 0.5
        w = self.largura(texto, fonte, tamanho)
        if alinhar == "dir":
            x -= w
        elif alinhar == "centro":
            x -= w / 2
        self.page.insert_text((x, y), texto, fontname=fonte, fontsize=tamanho)

    def faixa(self, x0, y0, x1, y1, cor):
        self.page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=None, fill=cor, width=0)


def centro(col):
    return (col[0] + col[1]) / 2


def gerar(dados, saida):
    doc = fitz.open(BASE)
    p = Pagina(doc[0])

    # --- Segurado e local de risco -----------------------------------------
    p.texto(LEFT, 217.2, dados["segurado"].strip().upper(), "bold", 11, max_w=RIGHT - LEFT)
    p.texto(LEFT, 250.0, "COTAÇÃO DE SEGURO RESIDENCIAL", "bold", 11)
    local = "LOCAL DE RISCO: – " + dados["local_risco"].strip()
    p.texto(LEFT, 263.5, local, "reg", 11, max_w=RIGHT - LEFT)

    # --- Cabeçalho da tabela -----------------------------------------------
    p.texto(302.6, 345.5, "Característica do Risco", "bold", 11, alinhar="centro")
    p.faixa(COL_COBERTURA[0], CAB_TOPO, COL_VALOR[1], CAB_BASE, AZUL_ESCURO)
    p.faixa(COL_POS[0], CAB_TOPO, COL_MINIMO[1], CAB_MEIO, AZUL_ESCURO)
    p.faixa(COL_POS[0], CAB_MEIO, COL_MINIMO[1], CAB_BASE, AZUL_CLARO)
    p.texto(centro(COL_COBERTURA), 377.0, "COBERTURAS", "bold", 11, alinhar="centro")
    p.texto(centro(COL_VALOR), 368.7, "VALOR", "bold", 11, alinhar="centro")
    p.texto(centro(COL_VALOR), 385.2, "MÁXIMO SEGURADO", "bold", 11, alinhar="centro")
    p.texto(centro((COL_POS[0], COL_MINIMO[1])), 362.2, "FRANQUIA", "bold", 11, alinhar="centro")
    p.texto(centro(COL_POS), 378.6, "POS (%", "bold", 11, alinhar="centro")
    p.texto(centro(COL_POS), 392.0, "Prejuízo)", "bold", 11, alinhar="centro")
    p.texto(centro(COL_MINIMO), 385.3, "Mínimo", "bold", 11, alinhar="centro")

    # --- Linhas de cobertura -----------------------------------------------
    topo = CAB_BASE
    for i, cob in enumerate(dados["coberturas"]):
        if i % 2 == 1:
            p.faixa(COL_COBERTURA[0], topo, COL_MINIMO[1], topo + ALTURA_LINHA, AZUL_CLARO)
        y = topo + 10.45
        nome = cob["nome"].strip().rstrip(":") + ":"
        p.texto(306.3, y, nome, "bold", 11, alinhar="dir", max_w=306.3 - 34.0)
        p.texto(311.7, y, "R$", "reg", 11)
        p.texto(408.2, y, cob["lmi"], "reg", 11, alinhar="dir")
        if cob.get("pos"):
            p.texto(455.0, y, cob["pos"], "reg", 11, alinhar="centro")
        if cob.get("minimo"):
            p.texto(535.3, y, cob["minimo"], "reg", 11, alinhar="dir")
        topo += ALTURA_LINHA
    fim_tabela = topo

    p.texto(169.6, fim_tabela + 22.9,
            "(*) POS = Participação Obrigatória do Segurado sobre os prejuízos sofridos em eventuais sinistros",
            "reg", 10)

    # --- Opções de pagamento -----------------------------------------------
    y = fim_tabela + 107.75
    p.texto(56.3, y, "OPÇÕES DE PAGAMENTO:", "reg", 11)
    y += 25.4
    for op in dados["pagamento"]:
        p.texto(85.5, y, op["parcelas"], "reg", 11, alinhar="dir")
        p.texto(97.0, y, "R$", "reg", 11)
        p.texto(168.4, y, op["valor"], "reg", 11, alinhar="dir")
        if op.get("descricao"):
            p.texto(196.9, y, op["descricao"], "reg", 11)
        y += 13.45

    doc.subset_fonts()
    doc.set_metadata({
        "title": f"Cotação de Seguro Residencial - {dados['segurado'].strip().upper()}",
        "author": "S.R. Martins Corretora de Seguros",
    })
    doc.save(saida, garbage=4, deflate=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--sobrescrever"]
    if len(args) != 2:
        sys.exit(__doc__)
    # A cotação feita à mão costuma ter o mesmo nome; nunca apague sem querer.
    if Path(args[1]).exists() and "--sobrescrever" not in sys.argv:
        sys.exit(f"Já existe um arquivo em {args[1]}. Escolha outro nome "
                 "ou rode de novo com --sobrescrever se o usuário confirmar.")
    with open(args[0], encoding="utf-8") as f:
        gerar(json.load(f), args[1])
    print(f"Cotação gerada: {args[1]}")
