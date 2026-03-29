import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="UniTrack", layout="centered")

st.markdown("---")
st.caption("Sistema inteligente de controle de faltas acadêmicas")


try:
    with open("data/materias.json", "r", encoding="utf-8") as f:
        materias_salvas = json.load(f)
except:
    materias_salvas = []

if "materias" not in st.session_state:
    st.session_state.materias = materias_salvas


def calcular_limite_faltas(aulas_semana):
    if aulas_semana == 1:
        return 8
    elif aulas_semana == 2:
        return 16
    elif aulas_semana == 3:
        return 18
    else:
        return aulas_semana * 8

def salvar_dados():
    os.makedirs("data", exist_ok=True)
    with open("data/materias.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.materias, f, indent=4, ensure_ascii=False)

# 🔥 atualização em tempo real
def atualizar_falta(index):
    st.session_state.materias[index]["faltas"] = st.session_state[f"faltas_{index}"]
    salvar_dados()


st.title("🎓 UniTrack - Controle de Faltas Acadêmicas")

st.header("👤 Dados do Aluno")
nome = st.text_input("Nome do aluno")
curso = st.text_input("Curso")
periodo = st.text_input("Período")

st.header("🏫 Faculdade")
st.info("Regras aplicadas: UNIRV Rio Verde")

st.header("📘 Cadastro da Matéria")
materia = st.text_input("Nome da matéria")
professor = st.text_input("Professor")
aulas_semana = st.selectbox("Quantidade de aulas por semana", [1, 2, 3])

limite_preview = calcular_limite_faltas(aulas_semana)
st.info(f"📌 Limite de faltas para essa matéria: {limite_preview}")

st.header("❌ Registro de Faltas")
faltas_input = st.number_input("Quantidade de faltas", min_value=0, step=1)

if st.button("➕ Adicionar Matéria"):
    if materia and professor:
        limite_faltas = calcular_limite_faltas(aulas_semana)

        materia_data = {
            "materia": materia,
            "professor": professor,
            "aulas_semana": aulas_semana,
            "faltas": faltas_input,
            "limite": int(limite_faltas)
        }

        st.session_state.materias.append(materia_data)
        salvar_dados()

        st.success("✅ Matéria adicionada!")
    else:
        st.error("Preencha todos os campos!")


if st.session_state.materias:
    total_faltas = sum(m["faltas"] for m in st.session_state.materias)
    total_limites = sum(m["limite"] for m in st.session_state.materias)

    col1, col2 = st.columns(2)
    col1.metric("Total de faltas", total_faltas)
    col2.metric("Limite total", total_limites)


st.header("📚 Suas Matérias")

if st.session_state.materias:
    for i, m in enumerate(st.session_state.materias):
        with st.container(border=True):
            col_top1, col_top2 = st.columns([5,1])

            with col_top1:
                st.subheader(f"📘 {m['materia']}")

            with col_top2:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.materias.pop(i)
                    salvar_dados()
                    st.rerun()

            st.write(f"👨‍🏫 {m['professor']}")
            st.write(f"📅 {m['aulas_semana']} aulas/semana")

            faltas = m["faltas"]
            limite = m["limite"]

            
            st.number_input(
                "Faltas",
                min_value=0,
                value=faltas,
                key=f"faltas_{i}",
                on_change=atualizar_falta,
                args=(i,)
            )

            faltas_atual = st.session_state.materias[i]["faltas"]
            restantes = limite - faltas_atual

            percentual = (faltas_atual / limite) * 100 if limite > 0 else 0

            st.progress(min(percentual / 100, 1.0))
            st.write(f"📊 {faltas_atual} / {limite} faltas ({percentual:.1f}%)")

            if faltas_atual < limite * 0.7:
                st.success("🟢 Tranquilo")
            elif faltas_atual < limite:
                st.warning("🟡 Atenção!")
            else:
                st.error("🔴 Reprovado")

            if restantes > 0:
                st.write(f"📉 Restam {int(restantes)} faltas")
            else:
                st.error("⚠️ Limite atingido!")

            if restantes <= 2 and restantes > 0:
                st.warning("⚠️ Cuidado! Quase no limite!")

            if m["aulas_semana"] > 0:
                semanas_restantes = restantes / m["aulas_semana"]
                st.caption(f"⏳ {semanas_restantes:.1f} semanas sem faltar")
else:
    st.info("Nenhuma matéria cadastrada.")



st.markdown("---")
st.caption("Desenvolvido para ajudar estudantes a evitarem reprovação por falta 📚")
