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

        os.makedirs("data", exist_ok=True)

        with open("data/materias.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.materias, f, indent=4, ensure_ascii=False)

        st.success("✅ Matéria adicionada!")
    else:
        st.error("Preencha todos os campos!")

st.header("📚 Suas Matérias")

if st.session_state.materias:
    for i, m in enumerate(st.session_state.materias):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(f"📘 {m['materia']}")
            st.write(f"👨‍🏫 Professor: {m['professor']}")
            st.write(f"📅 Aulas por semana: {m['aulas_semana']}")
            st.write(f"📊 Faltas: {m['faltas']} / {m['limite']}")

            faltas = m["faltas"]
            limite = m["limite"]
            restantes = limite - faltas

            if faltas < limite * 0.7:
                st.success("🟢 Tranquilo")
            elif faltas < limite:
                st.warning("🟡 Atenção! Você está chegando perto do limite de faltas.")
            else:
                st.error("🔴 Reprovado por falta!")

            if restantes > 0:
                st.write(f"📉 Restam {int(restantes)} faltas possíveis")
            else:
                st.error("⚠️ Limite atingido!")

        with col2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.materias.pop(i)

                with open("data/materias.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.materias, f, indent=4, ensure_ascii=False)

                st.rerun()
else:
    st.info("Nenhuma matéria cadastrada.")

st.markdown("### 📊 Gráfico de Faltas")

if st.session_state.materias:
    df = pd.DataFrame(st.session_state.materias)

    if not df.empty:
        df_plot = df[["materia", "faltas", "limite"]].set_index("materia")
        st.bar_chart(df_plot)
else:
    st.info("Adicione matérias para ver o gráfico.")

st.markdown("---")
st.caption("Desenvolvido para ajudar estudantes a evitarem reprovação por falta 📚")