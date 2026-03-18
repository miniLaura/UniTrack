import streamlit as st
import json

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
faltas = st.number_input("Quantidade de faltas", min_value=0, step=1)

if st.button("Calcular Situação"):

    limite_faltas = total_aulas * (limite_percentual / 100)
    restantes = limite_faltas - faltas

    st.subheader("📊 Resultado")

    st.write(f"Aluno: {nome}")
    st.write(f"Matéria: {materia}")
    st.write(f"Professor: {professor}")

    st.write(f"Total de aulas: {total_aulas}")
    st.write(f"Limite de faltas: {int(limite_faltas)}")
    st.write(f"Faltas atuais: {faltas}")

    if faltas < limite_faltas * 0.7:
        st.success("🟢 Situação: Tranquilo")
    elif faltas < limite_faltas:
        st.warning("🟡 Atenção! Você está perto do limite.")
    else:
        st.error("🔴 Reprovado por falta!")

    st.write(f"Você ainda pode faltar: {max(0, int(restantes))}")