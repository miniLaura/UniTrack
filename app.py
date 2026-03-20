import streamlit as st
import json
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
import os


if os.path.exists("data/materias.json"):
    with open("data/materias.json", "r", encoding="utf-8") as f:
        materias_salvas = json.load(f)
else:
    materias_salvas = []

if "materias" not in st.session_state:
    st.session_state.materias = materias_salvas

with open("data/regras_faculdade.json", "r", encoding="utf-8") as f:
    regras = json.load(f)

st.set_page_config(page_title="UniTrack", layout="centered")

st.title("🎓 UniTrack - Controle de Faltas Acadêmicas")


st.header("👤 Dados do Aluno")
nome = st.text_input("Nome do aluno")
curso = st.text_input("Curso")
periodo = st.text_input("Período")


st.header("🏫 Faculdade")

faculdade = st.selectbox("Selecione sua faculdade", list(regras.keys()))

limite_percentual = regras[faculdade]["limite_faltas"] * 100

st.write(f"📌 Limite de faltas dessa faculdade: {int(limite_percentual)}%")



st.header("📘 Cadastro da Matéria")

materia = st.text_input("Nome da matéria")
professor = st.text_input("Professor")
total_aulas = st.number_input("Total de aulas", min_value=1, step=1)


st.header("❌ Registro de Faltas")

faltas_input = st.number_input("Quantidade de faltas", min_value=0, step=1)


if st.button("➕ Adicionar Matéria"):

    if materia and professor:

        limite_faltas = total_aulas * (limite_percentual / 100)

        materia_data = {
            "materia": materia,
            "professor": professor,
            "total_aulas": total_aulas,
            "faltas": faltas_input,
            "limite": int(limite_faltas)
        }

        st.session_state.materias.append(materia_data)


        with open("data/materias.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.materias, f, indent=4, ensure_ascii=False)

        st.success("✅ Matéria adicionada e salva!")

    else:
        st.error("Preencha todos os campos!")

st.header("📊 Análise Geral")

if st.session_state.materias:

    nomes = [m["materia"] for m in st.session_state.materias]
    faltas = [m["faltas"] for m in st.session_state.materias]
    limites = [m["limite"] for m in st.session_state.materias]
    

    x = range(len(nomes))

    fig, ax = plt.subplots(figsize=(10, 5))


    ax.bar(x, faltas, width=0.4, label="Faltas")
    ax.bar([i + 0.4 for i in x], limites, width=0.4, label="Limite")

    ax.set_xticks([i + 0.2 for i in x])
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.set_xticklabels(nomes)

    ax.set_title(" Comparação de Faltas por Matéria", fontsize=14, fontweight="bold")
    ax.set_ylabel("Quantidade de Aulas")

    ax.legend()


    for i, limite in enumerate(limites):
        alerta = limite * 0.7
        ax.axhline(y=alerta, linestyle="--", alpha=0.2)

    st.pyplot(fig)

else:
    st.info("Adicione matérias para ver o gráfico.")

