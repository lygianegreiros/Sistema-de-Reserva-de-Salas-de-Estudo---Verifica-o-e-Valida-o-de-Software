"""Gera o Relatório Final em PDF da Atividade de Recuperação – VV."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registra a fonte Arial (todas as variantes) a partir do Windows.
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", r"C:\Windows\Fonts\arialbi.ttf"))
# Vincula as variantes para que <b> e <i> funcionem nos Paragraphs.
pdfmetrics.registerFontFamily(
    "Arial", normal="Arial", bold="Arial-Bold",
    italic="Arial-Italic", boldItalic="Arial-BoldItalic",
)

OUTPUT = "Relatorio_VV_Reserva_Salas.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm,
)

styles = getSampleStyleSheet()
W = A4[0] - 4 * cm  # largura útil

BLACK = colors.black

titulo = ParagraphStyle("titulo", parent=styles["Title"], fontName="Arial-Bold",
                        fontSize=16, textColor=BLACK, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Arial-Bold",
                    fontSize=13, textColor=BLACK, spaceAfter=4)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Arial-Bold",
                    fontSize=11, textColor=BLACK, spaceAfter=3)
normal = ParagraphStyle("normal", parent=styles["Normal"], fontName="Arial",
                        fontSize=10, leading=14, textColor=BLACK, spaceAfter=4,
                        alignment=TA_JUSTIFY)
code = ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                      fontSize=8, leading=11, textColor=BLACK, spaceAfter=4,
                      backColor=colors.HexColor("#f4f4f4"), borderPadding=(4, 6, 4, 6))
center = ParagraphStyle("center", parent=styles["Normal"], fontName="Arial",
                        fontSize=10, textColor=BLACK, alignment=TA_CENTER)

# Estilos para o CONTEÚDO das células das tabelas (garantem quebra de linha).
cell = ParagraphStyle("cell", fontName="Arial", fontSize=8, leading=10,
                      textColor=BLACK, alignment=TA_LEFT)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Arial-Bold", fontSize=8.5,
                          leading=10, textColor=BLACK, alignment=TA_CENTER)

HDR_BG  = colors.HexColor("#d9d9d9")   # cinza claro (texto preto legível)
ROW_ALT = colors.HexColor("#f2f2f2")   # zebra bem clara
WHITE   = colors.white


def P(texto, estilo=cell):
    """Envolve o texto em Paragraph para que quebre linha dentro da célula."""
    return Paragraph(texto, estilo)


def table_style(has_header=True):
    cmds = [
        ("FONTNAME",  (0, 0), (-1, -1), "Arial"),
        ("FONTSIZE",  (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
        ("ROWBACKGROUND", (0, 0), (-1, -1), [WHITE, ROW_ALT]),
        ("GRID",      (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]
    if has_header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HDR_BG),
            ("TEXTCOLOR",  (0, 0), (-1, 0), BLACK),
            ("FONTNAME",   (0, 0), (-1, 0), "Arial-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 9),
        ]
    return TableStyle(cmds)

story = []

# ── CAPA ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5 * cm))
story.append(Paragraph("Atividade de Recuperação", titulo))
story.append(Paragraph("Verificação e Validação de Software", titulo))
story.append(HRFlowable(width=W, thickness=2, color=BLACK, spaceAfter=8))
story.append(Paragraph("Sistema de Reserva de Salas de Estudo", h1))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Aluna: Lygian Monteiro", normal))
story.append(Paragraph("Disciplina: Verificação e Validação de Software", normal))
story.append(Paragraph("Data: 30/06/2025", normal))
story.append(Spacer(1, 0.6 * cm))

# ── 1. REQUISITOS ─────────────────────────────────────────────────────────────
story.append(Paragraph("1. Requisitos do Sistema", h1))
story.append(Paragraph(
    "O sistema gerencia reservas de salas de estudo de uma instituição de ensino. "
    "Anteriormente as reservas eram feitas em planilhas pela secretaria, gerando "
    "problemas de duplicidade e falta de histórico. Os requisitos levantados foram:", normal))

story.append(Paragraph("1.1 Requisitos Funcionais (RF)", h2))
rf_data = [
    ["Código", "Descrição"],
    ["RF01", "O sistema deve permitir o cadastro de um novo aluno."],
    ["RF02", "O sistema deve permitir consultar as salas disponíveis."],
    ["RF03", "O aluno deve poder realizar uma reserva de sala."],
    ["RF04", "O sistema deve impedir reservas para horários já ocupados."],
    ["RF05", "O sistema deve permitir consultar o histórico de reservas realizadas."],
]
rf_table = Table(rf_data, colWidths=[2.2 * cm, W - 2.2 * cm])
rf_table.setStyle(table_style())
story.append(rf_table)
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph("1.2 Requisitos Não Funcionais (RNF)", h2))
rnf_data = [
    ["Código", "Descrição"],
    ["RNF01", "O sistema deve ser implementado na linguagem Python."],
    ["RNF02", "O código deve ser modularizado, com separação entre lógica e testes."],
    ["RNF03", "O tempo de resposta das funções deve ser inferior a 3 segundos."],
]
rnf_table = Table(rnf_data, colWidths=[2.2 * cm, W - 2.2 * cm])
rnf_table.setStyle(table_style())
story.append(rnf_table)
story.append(Spacer(1, 0.5 * cm))

# ── 2. PLANO DE TESTES ────────────────────────────────────────────────────────
story.append(Paragraph("2. Plano de Testes Funcionais", h1))
story.append(Paragraph(
    "Os casos de teste abaixo cobrem todos os requisitos funcionais. "
    "Os resultados obtidos são reais, gerados pela execução do pytest.", normal))

ct_data = [
    ["ID", "Objetivo", "Entrada", "Resultado Esperado", "Resultado Obtido", "Status"],
    ["CT01", "Cadastrar aluno válido (RF01)",
     "Matrícula='2024001', Nome='Ana Silva'",
     "sucesso=True, mensagem contém 'Ana Silva'",
     "sucesso=True, mensagem='Aluno Ana Silva cadastrado com sucesso.'",
     "Aprovado"],
    ["CT02", "Rejeitar matrícula duplicada (RF01)",
     "Matrícula='2024001' já cadastrada",
     "sucesso=False, mensagem 'já cadastrada'",
     "sucesso=False, mensagem='Matrícula já cadastrada.'",
     "Aprovado"],
    ["CT03", "Rejeitar cadastro com campos vazios (RF01)",
     "Matrícula='' ou Nome=''",
     "sucesso=False",
     "sucesso=False para ambos os casos",
     "Aprovado"],
    ["CT04", "Consultar salas sem reservas (RF02)",
     "Data='2025-07-01', Horário='08:00' (sem reservas)",
     "Lista com todas as 5 salas",
     "Lista retornou as 5 salas cadastradas",
     "Aprovado"],
    ["CT05", "Realizar reserva válida (RF03)",
     "Aluno cadastrado, Sala 1, 2025-07-01, 08:00",
     "sucesso=True, mensagem contém 'Sala 1'",
     "sucesso=True, mensagem='Reserva realizada: Sala 1 em 2025-07-01 às 08:00.'",
     "Aprovado"],
    ["CT06", "Bloquear reserva duplicada (RF04)",
     "Sala 2, 2025-07-01, 10:00 já reservada",
     "sucesso=False, mensagem 'já reservado'",
     "sucesso=False, mensagem='Horário já reservado para esta sala.'",
     "Aprovado"],
    ["CT07", "Consultar histórico do aluno (RF05)",
     "Aluno com 2 reservas realizadas",
     "Lista com 2 reservas",
     "Retornou lista com 2 registros corretos",
     "Aprovado"],
    ["CT08", "Histórico de aluno inexistente (RF05)",
     "Matrícula='9999999' não cadastrada",
     "Lista vazia []",
     "Retornou []",
     "Aprovado"],
    ["CT09", "Sala ocupada some da disponibilidade (RF02+RF04)",
     "Sala 1 reservada para 2025-07-01, 08:00",
     "Sala 1 não aparece na lista de disponíveis",
     "Sala 1 ausente da listagem de disponíveis",
     "Aprovado"],
    ["CT10", "Rejeitar reserva de aluno não cadastrado (RF03)",
     "Matrícula='9999999' não cadastrada",
     "sucesso=False, mensagem 'não cadastrado'",
     "sucesso=False, mensagem='Aluno não cadastrado.'",
     "Aprovado"],
    ["CT11", "Rejeitar reserva em sala inexistente (RF03)",
     "Aluno cadastrado, Sala='Sala 99'",
     "sucesso=False, mensagem 'inexistente'",
     "sucesso=False, mensagem='Sala inexistente.'",
     "Aprovado"],
]

# Envolve cada célula em Paragraph para que o texto quebre linha dentro da coluna
# (evita que as colunas fiquem "quebradas"/sobrepostas). O cabeçalho fica centralizado.
ct_render = [[P(txt, cell_hdr) for txt in ct_data[0]]]
for linha in ct_data[1:]:
    ct_render.append([P(txt, cell) for txt in linha])

col_w = [1.1*cm, 3.0*cm, 3.3*cm, 3.8*cm, 4.0*cm, 1.8*cm]  # soma = 17 cm (largura útil)
ct_table = Table(ct_render, colWidths=col_w, repeatRows=1)
ct_table.setStyle(table_style())
ct_table.setStyle(TableStyle([
    ("BACKGROUND", (5, 1), (5, -1), colors.HexColor("#e2efda")),  # verde bem claro
    ("ALIGN",      (0, 0), (0, -1), "CENTER"),                    # coluna ID centralizada
]))
story.append(ct_table)
story.append(Spacer(1, 0.5 * cm))

# ── 3. TESTES AUTOMATIZADOS ───────────────────────────────────────────────────
story.append(Paragraph("3. Testes Automatizados (pytest)", h1))
story.append(Paragraph(
    "Os testes foram escritos no arquivo <b>test_reserva_salas.py</b> utilizando o framework "
    "pytest. O sistema é implementado como a classe <b>SistemaReservas</b>; cada teste recebe "
    "uma instância nova e vazia através da <i>fixture</i> <b>sistema</b>, garantindo isolamento "
    "completo entre os casos (um teste nunca interfere no outro).", normal))

story.append(Paragraph("3.1 Trecho do código de testes", h2))
trecho = """@pytest.fixture
def sistema():
    \"\"\"Cria um sistema novo e vazio para cada teste (isolamento).\"\"\"
    return SistemaReservas()

# CT05 – RF03: Reserva válida é aceita
def test_reserva_valida(sistema):
    \"\"\"Aluno cadastrado consegue reservar uma sala disponível.\"\"\"
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    resultado = sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00")
    assert resultado["sucesso"] is True
    assert "Sala 1" in resultado["mensagem"]

# CT06 – RF04: Reserva para horário já ocupado deve ser bloqueada
def test_reserva_horario_ocupado(sistema):
    \"\"\"O sistema deve impedir uma segunda reserva no mesmo sala/data/horário.\"\"\"
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    sistema.cadastrar_aluno("2024002", "Bruno Costa")
    sistema.realizar_reserva("2024001", "Sala 2", "2025-07-01", "10:00")
    resultado = sistema.realizar_reserva("2024002", "Sala 2", "2025-07-01", "10:00")
    assert resultado["sucesso"] is False
    assert "já reservado" in resultado["mensagem"]"""
story.append(Paragraph(trecho.replace("\n", "<br/>"), code))

story.append(Paragraph("3.2 Resultado da execução do pytest", h2))
resultado_pytest = """$ python -m pytest test_reserva_salas.py -v
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1
collected 11 items

test_reserva_salas.py::test_cadastro_aluno_valido              PASSED  [  9%]
test_reserva_salas.py::test_cadastro_matricula_duplicada       PASSED  [ 18%]
test_reserva_salas.py::test_cadastro_campos_vazios             PASSED  [ 27%]
test_reserva_salas.py::test_salas_disponiveis_sem_reservas     PASSED  [ 36%]
test_reserva_salas.py::test_reserva_valida                     PASSED  [ 45%]
test_reserva_salas.py::test_reserva_horario_ocupado            PASSED  [ 54%]
test_reserva_salas.py::test_historico_reservas                 PASSED  [ 63%]
test_reserva_salas.py::test_historico_aluno_inexistente        PASSED  [ 72%]
test_reserva_salas.py::test_sala_ocupada_nao_aparece_como_disponivel PASSED  [ 81%]
test_reserva_salas.py::test_reserva_aluno_nao_cadastrado       PASSED  [ 90%]
test_reserva_salas.py::test_reserva_sala_inexistente           PASSED  [100%]

============================= 11 passed in 0.06s =============================="""
story.append(Paragraph(resultado_pytest.replace("\n", "<br/>"), code))
story.append(Spacer(1, 0.5 * cm))

# ── 4. COBERTURA ──────────────────────────────────────────────────────────────
story.append(Paragraph("4. Cobertura de Testes", h1))

story.append(Paragraph("4.1 Relatório gerado pelo pytest-cov", h2))
cobertura = """$ python -m pytest test_reserva_salas.py --cov=reserva_salas --cov-report=term-missing

Name               Stmts   Miss  Cover   Missing
------------------------------------------------
reserva_salas.py      29      0   100%
------------------------------------------------
TOTAL                 29      0   100%"""
story.append(Paragraph(cobertura.replace("\n", "<br/>"), code))

story.append(Paragraph("4.2 Análise da cobertura", h2))
story.append(Paragraph(
    "<b>Cobertura atingida: 100%</b> (todas as 29 linhas executáveis da lógica cobertas "
    "pelos testes).", normal))
story.append(Paragraph(
    "<b>O que está coberto:</b> Todos os métodos da classe <i>SistemaReservas</i> foram "
    "exercitados — <i>cadastrar_aluno</i>, <i>consultar_salas_disponiveis</i>, "
    "<i>realizar_reserva</i> e <i>consultar_historico</i>. Foram testados tanto os caminhos "
    "de sucesso quanto todos os caminhos de erro (matrícula duplicada, campos vazios, "
    "conflito de horário, aluno não cadastrado e sala inexistente).", normal))
story.append(Paragraph(
    "<b>O que não está coberto:</b> Apenas o bloco de demonstração <i>if __name__ == "
    "'__main__'</i> ficou de fora, o que é intencional — ele serve apenas para execução "
    "manual e foi marcado com <i># pragma: no cover</i>, pois não faz parte da lógica de "
    "negócio testável.", normal))
story.append(Spacer(1, 0.5 * cm))

# ── 5. CONCLUSÃO ──────────────────────────────────────────────────────────────
story.append(Paragraph("5. Conclusão e Avaliação Crítica", h1))
story.append(Paragraph(
    "O sistema desenvolvido atende a todos os cinco requisitos funcionais definidos no documento "
    "de requisitos. A implementação foi realizada em Python puro, sem dependências externas, "
    "respeitando o RNF01. A separação entre o módulo de lógica (<i>reserva_salas.py</i>, com a "
    "classe <i>SistemaReservas</i>) e o arquivo de testes (<i>test_reserva_salas.py</i>) atende "
    "ao RNF02. O tempo de execução dos 11 testes foi de 0,06 segundos, muito abaixo do limite "
    "de 3 segundos do RNF03.", normal))
story.append(Paragraph(
    "A cobertura de 100% indica que todas as ramificações da lógica de negócio foram "
    "exercitadas pelos testes automatizados, incluindo os caminhos de sucesso e todos os "
    "caminhos de erro. Isso dá alta confiança de que o comportamento do sistema corresponde "
    "ao especificado nos requisitos.", normal))
story.append(Paragraph(
    "<b>Pontos de melhoria identificados:</b> O sistema atualmente armazena dados em memória "
    "(listas e dicionários Python), o que significa que os dados são perdidos ao encerrar o "
    "programa. Uma evolução natural seria persistir os dados em banco de dados ou arquivo JSON. "
    "Além disso, não há validação de formato de data/horário, o que poderia causar reservas "
    "com entradas inválidas em um ambiente de produção.", normal))
story.append(Paragraph(
    "Em síntese, o sistema cumpre seu papel pedagógico de demonstrar a aplicação de técnicas "
    "de Verificação e Validação: análise de requisitos, elaboração de plano de testes, "
    "automação com pytest e medição de cobertura.", normal))

doc.build(story)
print(f"PDF gerado: {OUTPUT}")
