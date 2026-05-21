# 🎓 UniTrack

Sistema simples para controlar notas e frequência por semestre.

## O que ele faz

- Cadastro de aluno, curso e semestre
- Cadastro de disciplinas
- Lançamento de N1, N2 e N3
- Cálculo da média oficial: `(N1 + N2 + N3) / 3`
- Alerta de aprovação com média mínima 60
- Calculadora de quanto precisa tirar nas próximas avaliações
- Controle de faltas com presença mínima de 75%
- Regra de faltas por quantidade de aulas na semana:
  - 1 aula/semana = 2 créditos = até 8 faltas
  - 2 aulas/semana = 4 créditos = até 16 faltas
  - 3 aulas/semana = 6 créditos = até 18 faltas
- Backup por exportação/importação JSON
- Dados salvos no navegador usando `localStorage`

## Rodando com Streamlit

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Para Streamlit Cloud, mantenha no repositório:

- `app.py`
- `index.html`
- `requirements.txt`

