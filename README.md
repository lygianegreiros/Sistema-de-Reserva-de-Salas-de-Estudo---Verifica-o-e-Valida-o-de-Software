# 🏫 Sistema de Reserva de Salas de Estudo

Projeto desenvolvido para a atividade de **Verificação e Validação de Software**.
O sistema gerencia a reserva de salas de estudo de uma instituição de ensino, substituindo o antigo controle manual feito em planilhas — que causava reservas duplicadas e falta de histórico.

O foco do projeto está na **qualidade de software**: análise de requisitos, testes automatizados e cobertura de testes.

---

## 📋 Sobre o projeto

O sistema permite:

- 👤 Cadastrar alunos
- 🔍 Consultar salas disponíveis
- 📅 Reservar uma sala
- 🚫 Impedir reservas em horários já ocupados
- 📖 Consultar o histórico de reservas

---

## ✅ Requisitos atendidos

### Requisitos Funcionais (RF)

| Código | Descrição | Onde está no código |
|--------|-----------|---------------------|
| RF01 | Cadastrar um novo aluno | `cadastrar_aluno()` |
| RF02 | Consultar as salas disponíveis | `consultar_salas_disponiveis()` |
| RF03 | Realizar uma reserva de sala | `realizar_reserva()` |
| RF04 | Impedir reservas para horários já ocupados | `realizar_reserva()` (regra de conflito) |
| RF05 | Consultar o histórico de reservas | `consultar_historico()` |

### Requisitos Não Funcionais (RNF)

| Código | Descrição | Como foi atendido |
|--------|-----------|-------------------|
| RNF01 | Implementado em Python | ✅ Python puro, sem dependências externas na lógica |
| RNF02 | Código modularizado (lógica separada dos testes) | ✅ `reserva_salas.py` (lógica) + `test_reserva_salas.py` (testes) |
| RNF03 | Tempo de resposta inferior a 3 segundos | ✅ Todos os testes rodam em ~0,06s |

---

## 📁 Estrutura do projeto

```
reserva-salas-vv/
├── README.md                       # Este arquivo
├── reserva_salas.py                # Lógica do sistema (classe SistemaReservas)
├── test_reserva_salas.py           # Testes automatizados (pytest)
├── Relatorio_VV_Reserva_Salas.pdf  # Relatório final da atividade
└── gerar_relatorio.py              # Script que gera o relatório em PDF
```

---

## 🚀 Como executar

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado
- Instalar as bibliotecas de teste:

```bash
pip install pytest pytest-cov
```

### 1. Rodar o sistema (demonstração)

```bash
python reserva_salas.py
```

### 2. Rodar os testes automatizados

```bash
python -m pytest test_reserva_salas.py -v
```

### 3. Gerar o relatório de cobertura de testes

```bash
python -m pytest test_reserva_salas.py --cov=reserva_salas --cov-report=term-missing
```

---

## 🧪 Testes e cobertura

O projeto conta com **11 testes automatizados** escritos com **pytest**, cobrindo tanto os
caminhos de sucesso quanto os de erro (matrícula duplicada, campos vazios, conflito de
horário, aluno não cadastrado e sala inexistente).

| Métrica | Resultado |
|---------|-----------|
| Testes executados | 11 |
| Testes aprovados | ✅ 11/11 |
| Cobertura de código | 🎯 **100%** da lógica de negócio |
| Tempo de execução | ~0,06 segundos |

> Cada teste recebe uma instância nova e vazia do sistema através de uma *fixture* do pytest,
> garantindo isolamento total entre os casos de teste.

---

## 📄 Relatório completo

O documento **[Relatorio_VV_Reserva_Salas.pdf](Relatorio_VV_Reserva_Salas.pdf)** contém:

- Requisitos (RF e RNF)
- Plano de testes funcionais (casos CT01 a CT11)
- Evidências de testes (trechos de código e saída do pytest)
- Cobertura de testes e análise
- Conclusão com avaliação crítica da qualidade do sistema

---

## 👩‍💻 Autora

**Lygian Monteiro**
Atividade de Recuperação — Verificação e Validação de Software
