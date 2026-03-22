st.write(os.listdir())
st.write(os.listdir("data"))
import streamlit as st
import json
import pandas as pd
import os


try:
    with open("data/materias.json", "r", encoding="utf-8") as f:
        materias_salvas = json.load(f)
except:
    materias_salvas = []

if "materias" not in st.session_state:
    st.session_state.materias = materias_salvas


try:
    with open("data/regras_faculdade.json", "r", encoding="utf-8") as f:
        regras = json.load(f)
except:
    regras = {
        "Faculdade Padrão": {"limite_faltas": 0.25}
    }


st.set_page_config(page_title="UniTrack", layout="centered")

st.title("🎓 UniTrack - Controle de Faltas Acadêmicas")
st.markdown("---")

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

if st.button("🗑️ Limpar todas as matérias"):

    st.session_state.materias = []

    with open("data/materias.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    st.success("Todas as matérias foram removidas!")

    
st.markdown("### 📈 Visualização Geral")
st.header("📊 Análise")

st.markdown("### 📊 Gráfico de Faltas")

if st.session_state.materias:

    df = pd.DataFrame(st.session_state.materias)

    df_plot = df[["materia", "faltas", "limite"]]
    df_plot = df_plot.set_index("materia")

    st.bar_chart(df_plot)

else:
    st.info("Adicione matérias para ver o gráfico.")


st.header("📚 Suas Matérias")

if st.session_state.materias:

    for i, m in enumerate(st.session_state.materias):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(m["materia"])
            st.write(f"👨‍🏫 Professor: {m['professor']}")
            st.write(f"📊 Faltas: {m['faltas']} / {m['limite']}")

        with col2:
            if st.button("❌", key=f"del_{i}"):

                st.session_state.materias.pop(i)

                with open("data/materias.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.materias, f, indent=4, ensure_ascii=False)

                st.rerun()