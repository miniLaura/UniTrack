import streamlit as st
import json
import pandas as pd
import os


st.markdown("---")
st.caption("Sistema inteligente de controle de faltas acadêmicas")

try:
    with open("data/materias.json", "r", encoding="utf-8") as f:
        materias_salvas = json.load(f)
except:
    materias_salvas = []

if "materias" not in st.session_state:
    st.session_state.materias = materias_salvas



if os.path.exists("data/regras_faculdade.json"):
    with open("data/regras_faculdade.json", "r", encoding="utf-8") as f:
        regras = json.load(f)
else:
    regras = {}



st.set_page_config(page_title="UniTrack", layout="centered")

st.title("🎓 UniTrack - Controle de Faltas Acadêmicas")



st.header("👤 Dados do Aluno")
nome = st.text_input("Nome do aluno")
curso = st.text_input("Curso")
periodo = st.text_input("Período")




st.header("🏫 Faculdade")

if regras:
    faculdade = st.selectbox("Selecione sua faculdade", list(regras.keys()))
    limite_percentual = regras[faculdade]["limite_faltas"] * 100
    st.write(f"📌 Limite de faltas: {int(limite_percentual)}%")
else:
    st.warning("⚠️ Arquivo de regras não encontrado.")
    faculdade = None
    limite_percentual = 25  # padrão




st.header("📘 Cadastro da Matéria")

materia = st.text_input("Nome da matéria")
professor = st.text_input("Professor")
total_aulas = st.number_input("Total de aulas", min_value=1, step=1)

st.header("❌ Registro de Faltas")
faltas_input = st.number_input("Quantidade de faltas", min_value=0, step=1)




if st.button("➕ Adicionar Matéria"):

    if materia and professor and total_aulas:

        limite_faltas = total_aulas * (limite_percentual / 100)

        materia_data = {
            "materia": materia,
            "professor": professor,
            "total_aulas": total_aulas,
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
            st.write(f"📊 Faltas: {m['faltas']} / {m['limite']}")

            faltas = m["faltas"]
            limite = m["limite"]
            restantes = limite - faltas

            # STATUS
            if faltas < limite * 0.7:
                st.success("🟢 Tranquilo")
            elif faltas < limite:
                st.warning("🟡 Atenção!")
            else:
                st.error("🔴 Reprovado por falta!")

            # RESTANTE
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