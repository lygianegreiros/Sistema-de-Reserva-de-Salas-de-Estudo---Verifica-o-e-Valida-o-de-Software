"""
Testes automatizados do Sistema de Reserva de Salas (pytest)
============================================================
Separado da lógica (atende ao RNF02). Cada teste corresponde a um caso
do Plano de Testes Funcionais (CT01 a CT10) e valida um Requisito Funcional.
"""

import pytest
from reserva_salas import SistemaReservas


@pytest.fixture
def sistema():
    """Cria um sistema novo e vazio para cada teste (garante isolamento)."""
    return SistemaReservas()


# CT01 – RF01: cadastro de aluno com dados válidos
def test_cadastro_aluno_valido(sistema):
    """Um aluno com matrícula e nome válidos deve ser cadastrado com sucesso."""
    resultado = sistema.cadastrar_aluno("2024001", "Ana Silva")
    assert resultado["sucesso"] is True
    assert "Ana Silva" in resultado["mensagem"]
    assert sistema.alunos["2024001"] == "Ana Silva"


# CT02 – RF01: cadastro com matrícula duplicada deve ser rejeitado
def test_cadastro_matricula_duplicada(sistema):
    """O sistema deve impedir cadastrar duas vezes a mesma matrícula."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    resultado = sistema.cadastrar_aluno("2024001", "Bruno Costa")
    assert resultado["sucesso"] is False
    assert "já cadastrada" in resultado["mensagem"]


# CT03 – RF01: cadastro com campos vazios deve ser rejeitado
def test_cadastro_campos_vazios(sistema):
    """Matrícula ou nome vazio deve ser recusado."""
    assert sistema.cadastrar_aluno("", "Carlos")["sucesso"] is False
    assert sistema.cadastrar_aluno("2024002", "")["sucesso"] is False


# CT04 – RF02: consulta de salas sem reservas retorna todas
def test_salas_disponiveis_sem_reservas(sistema):
    """Sem nenhuma reserva, todas as salas devem estar disponíveis."""
    disponiveis = sistema.consultar_salas_disponiveis("2025-07-01", "08:00")
    assert len(disponiveis) == len(sistema.salas)
    assert "Sala 1" in disponiveis


# CT05 – RF03: reserva válida é aceita
def test_reserva_valida(sistema):
    """Aluno cadastrado consegue reservar uma sala disponível."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    resultado = sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00")
    assert resultado["sucesso"] is True
    assert "Sala 1" in resultado["mensagem"]
    assert len(sistema.reservas) == 1


# CT06 – RF04: reserva para horário já ocupado deve ser bloqueada
def test_reserva_horario_ocupado(sistema):
    """O sistema deve impedir uma segunda reserva na mesma sala/data/horário."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    sistema.cadastrar_aluno("2024002", "Bruno Costa")
    sistema.realizar_reserva("2024001", "Sala 2", "2025-07-01", "10:00")
    resultado = sistema.realizar_reserva("2024002", "Sala 2", "2025-07-01", "10:00")
    assert resultado["sucesso"] is False
    assert "já reservado" in resultado["mensagem"]


# CT07 – RF05: histórico retorna as reservas do aluno
def test_historico_reservas(sistema):
    """O histórico deve conter todas as reservas do aluno consultado."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00")
    sistema.realizar_reserva("2024001", "Sala 3", "2025-07-02", "14:00")
    historico = sistema.consultar_historico("2024001")
    assert len(historico) == 2
    assert historico[0]["sala"] == "Sala 1"
    assert historico[1]["sala"] == "Sala 3"


# CT08 – RF05: histórico de aluno inexistente retorna lista vazia
def test_historico_aluno_inexistente(sistema):
    """Consulta de histórico para matrícula inexistente deve retornar []."""
    assert sistema.consultar_historico("9999999") == []


# CT09 – RF02+RF04: sala reservada não aparece como disponível
def test_sala_ocupada_nao_aparece_como_disponivel(sistema):
    """Após reservar, a sala não deve ser listada como disponível no mesmo horário."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00")
    disponiveis = sistema.consultar_salas_disponiveis("2025-07-01", "08:00")
    assert "Sala 1" not in disponiveis


# CT10 – RF03: reserva por aluno não cadastrado é rejeitada
def test_reserva_aluno_nao_cadastrado(sistema):
    """O sistema deve rejeitar reserva de aluno não cadastrado."""
    resultado = sistema.realizar_reserva("9999999", "Sala 1", "2025-07-01", "08:00")
    assert resultado["sucesso"] is False
    assert "não cadastrado" in resultado["mensagem"]


# CT11 – RF03: reserva em sala inexistente é rejeitada
def test_reserva_sala_inexistente(sistema):
    """O sistema deve rejeitar reserva para uma sala que não existe."""
    sistema.cadastrar_aluno("2024001", "Ana Silva")
    resultado = sistema.realizar_reserva("2024001", "Sala 99", "2025-07-01", "08:00")
    assert resultado["sucesso"] is False
    assert "inexistente" in resultado["mensagem"]
