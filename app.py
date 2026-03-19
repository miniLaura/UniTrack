import streamlit as st
import json
import matplotlib.pyplot as plt

if "materias" not in st.session_state:
    st.session_state.materias = []

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

        st.success("✅ Matéria adicionada com sucesso!")

    else:
        st.error("Preencha todos os campos!")


st.header("📊 Análise Geral")

if st.session_state.materias:

    nomes = [m["materia"] for m in st.session_state.materias]
    lista_faltas = [m["faltas"] for m in st.session_state.materias]
    limites = [m["limite"] for m in st.session_state.materias]

    fig, ax = plt.subplots()

    ax.bar(nomes, lista_faltas, label="Faltas")
    ax.bar(nomes, limites, alpha=0.3, label="Limite")

    ax.set_title("Faltas por Matéria")
    ax.set_ylabel("Quantidade")

    ax.legend()

    st.pyplot(fig)

else:
    st.info("Adicione matérias para ver o gráfico.")


if st.session_state.materias:

    total_faltas = sum([m["faltas"] for m in st.session_state.materias])
    total_limite = sum([m["limite"] for m in st.session_state.materias])

    st.subheader("📈 Resumo Geral")

    st.write(f"Total de faltas: {total_faltas}")
    st.write(f"Limite total: {total_limite}")

    if total_faltas < total_limite:
        st.success("🟢 Você ainda está dentro do limite geral!")
    else:
        st.error("🔴 Você ultrapassou o limite total!")