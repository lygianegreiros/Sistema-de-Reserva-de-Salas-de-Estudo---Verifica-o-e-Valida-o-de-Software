"""
Sistema de Reserva de Salas de Estudo
=====================================
Módulo de LÓGICA do sistema (separado dos testes — atende ao RNF02).

Cada método implementa um Requisito Funcional do Documento de Requisitos:
    RF01 -> cadastrar_aluno
    RF02 -> consultar_salas_disponiveis
    RF03 -> realizar_reserva
    RF04 -> realizar_reserva (regra de bloqueio de horário ocupado)
    RF05 -> consultar_historico
"""


class SistemaReservas:
    """Gerencia alunos e reservas de salas de estudo de uma instituição."""

    def __init__(self):
        # Estado do sistema mantido em memória.
        self.alunos = {}        # {matricula: nome}
        self.reservas = []       # [{matricula, sala, data, horario}]
        self.salas = ["Sala 1", "Sala 2", "Sala 3", "Sala 4", "Sala 5"]

    # ------------------------------------------------------------------ RF01
    def cadastrar_aluno(self, matricula: str, nome: str) -> dict:
        """RF01 – Permite o cadastro de um novo aluno.

        Regras:
        - Matrícula e nome são obrigatórios.
        - Não pode haver matrícula duplicada.
        """
        if not matricula or not nome:
            return {"sucesso": False, "mensagem": "Matrícula e nome são obrigatórios."}
        if matricula in self.alunos:
            return {"sucesso": False, "mensagem": "Matrícula já cadastrada."}

        self.alunos[matricula] = nome
        return {"sucesso": True, "mensagem": f"Aluno '{nome}' cadastrado com sucesso."}

    # ------------------------------------------------------------------ RF02
    def consultar_salas_disponiveis(self, data: str, horario: str) -> list:
        """RF02 – Retorna as salas livres para uma data e horário informados."""
        ocupadas = {
            r["sala"]
            for r in self.reservas
            if r["data"] == data and r["horario"] == horario
        }
        return [sala for sala in self.salas if sala not in ocupadas]

    # ------------------------------------------------------------- RF03 e RF04
    def realizar_reserva(self, matricula: str, sala: str, data: str, horario: str) -> dict:
        """RF03 – Permite ao aluno reservar uma sala.
        RF04 – Impede reservas para horários já ocupados.

        Regras:
        - O aluno precisa estar cadastrado.
        - A sala precisa existir.
        - Não pode existir outra reserva para a mesma sala/data/horário.
        """
        if matricula not in self.alunos:
            return {"sucesso": False, "mensagem": "Aluno não cadastrado."}
        if sala not in self.salas:
            return {"sucesso": False, "mensagem": "Sala inexistente."}

        # RF04 – verifica conflito de horário
        conflito = any(
            r["sala"] == sala and r["data"] == data and r["horario"] == horario
            for r in self.reservas
        )
        if conflito:
            return {"sucesso": False, "mensagem": "Horário já reservado para esta sala."}

        self.reservas.append({
            "matricula": matricula,
            "sala": sala,
            "data": data,
            "horario": horario,
        })
        return {
            "sucesso": True,
            "mensagem": f"Reserva realizada: {sala} em {data} às {horario}.",
        }

    # ------------------------------------------------------------------ RF05
    def consultar_historico(self, matricula: str) -> list:
        """RF05 – Retorna o histórico de reservas de um aluno.

        Aluno inexistente resulta em histórico vazio.
        """
        if matricula not in self.alunos:
            return []
        return [r for r in self.reservas if r["matricula"] == matricula]


# Execução manual simples para demonstração (não roda durante os testes).
if __name__ == "__main__":  # pragma: no cover
    sistema = SistemaReservas()
    print(sistema.cadastrar_aluno("2024001", "Ana Silva"))
    print(sistema.consultar_salas_disponiveis("2025-07-01", "08:00"))
    print(sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00"))
    print(sistema.realizar_reserva("2024001", "Sala 1", "2025-07-01", "08:00"))  # bloqueada
    print(sistema.consultar_historico("2024001"))
