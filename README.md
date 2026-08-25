# 🐞 Bug & Test Case Tracker

Mini aplicação web para gestão de **bugs e casos de teste**, construída em Python/Flask, simulando o fluxo de trabalho de QA que eu aplicava na prática (triagem de incidentes, severidade, status, passos para reprodução).

## 🎯 Objetivo

Demonstrar entendimento do ciclo de vida de um bug e de um caso de teste — não só documentar, mas ter uma ferramenta funcional onde é possível cadastrar, listar, filtrar e atualizar status.

## 🗂️ Estrutura

```
bug-test-case-tracker/
├── README.md
├── requirements.txt
├── app.py                  # Aplicação Flask (rotas e lógica)
├── schema.sql               # Schema do banco (SQLite)
├── seed_data.py              # Popula dados de exemplo
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── bugs_list.html
    ├── bug_form.html
    ├── testcases_list.html
    └── testcase_form.html
```

## 🧩 Modelo de dados

**Bug**
| Campo | Descrição |
|---|---|
| título | Resumo do problema |
| descrição | Detalhamento |
| severidade | Baixa / Média / Alta / Crítica |
| status | Aberto / Em andamento / Resolvido / Fechado |
| passos para reproduzir | Passo a passo do bug |
| ambiente | Onde foi identificado (produção, staging, navegador, etc.) |

**Caso de Teste**
| Campo | Descrição |
|---|---|
| título | Nome do teste |
| pré-condições | O que precisa estar pronto antes de rodar |
| passos | Passo a passo de execução |
| resultado esperado | O que deveria acontecer |
| status | Não executado / Passou / Falhou |

## 🛠️ Como rodar localmente

```bash
# 1. Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar o banco e popular com dados de exemplo
sqlite3 tracker.db < schema.sql
python seed_data.py

# 4. Rodar a aplicação
python app.py
```

Acesse em `http://localhost:5000`

## 📌 Competências demonstradas

- Modelagem de dados para processos de QA (bugs e casos de teste)
- Desenvolvimento web básico (Flask, SQLite, HTML/CSS)
- Entendimento do ciclo de vida de defeitos (severidade, status, triagem)
- Organização de informação para rastreabilidade

---
*Projeto desenvolvido por Ruan de Oliveira Alonso como parte de portfólio para vagas de QA / Analista de Sistemas.*
