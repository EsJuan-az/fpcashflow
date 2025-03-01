import streamlit as st
from datetime import date, timedelta
import pandas as pd

if 'contracts' not in st.session_state:
    st.session_state.contracts = []

def calcular_meses(inicio, fin):
    return (fin.year - inicio.year) * 12 + (fin.month - inicio.month)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Selecciona una sección", ("Administrar Contratos", "Calcular Liquidaciones"))

if pagina == "Administrar Contratos":
    st.title("Administrar Contratos")
    st.subheader("Registrar un nuevo contrato")

    with st.form("form_contrato", clear_on_submit=True):
        tipo_contrato = st.selectbox("Tipo de contrato", options=["Empleado", "Proveedor", "Colaborador", "Otro"])
        fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
        duracion_dias = st.number_input("Duración del contrato (días)", min_value=1, value=30)
        monto = st.number_input("Monto / Salario", min_value=0.0, value=1000.0, format="%.2f")
        contrato_file = st.file_uploader("Adjuntar contrato (PDF/Imagen)", type=["pdf", "png", "jpg", "jpeg"])
        enviar = st.form_submit_button("Registrar contrato")

    if enviar:
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        nuevo_contrato = {
            "Tipo": tipo_contrato,
            "Fecha inicio": fecha_inicio,
            "Fecha fin": fecha_fin,
            "Monto": monto,
            "Archivo": contrato_file.name if contrato_file else "No adjunto"
        }
        st.session_state.contracts.append(nuevo_contrato)
        st.success("Contrato registrado exitosamente.")

    st.subheader("Listado de Contratos")
    if st.session_state.contracts:
        df_contratos = pd.DataFrame(st.session_state.contracts)
        st.dataframe(df_contratos)

        proximos_vencer = []
        for contrato in st.session_state.contracts:
            if isinstance(contrato["Fecha fin"], date):
                dias_restantes = (contrato["Fecha fin"] - date.today()).days
                if dias_restantes <= 5:
                    contrato["Días restantes"] = dias_restantes
                    proximos_vencer.append(contrato)
        if proximos_vencer:
            st.warning("Alerta: Existen contratos próximos a vencer:")
            st.write(pd.DataFrame(proximos_vencer))
    else:
        st.info("No hay contratos registrados.")

elif pagina == "Calcular Liquidaciones":
    st.title("Calcular Liquidaciones")
    st.subheader("Calcular liquidación de un contrato finalizado")

    with st.form("form_liquidacion", clear_on_submit=True):
        tipo_contrato = st.selectbox("Tipo de contrato", options=["Empleado", "Colaborador", "Otro"])
        salario = st.number_input("Salario / Monto mensual", min_value=0.0, value=1000.0, format="%.2f")
        fecha_inicio_contrato = st.date_input("Fecha de inicio del contrato", value=date(2023, 1, 1))
        fecha_fin_contrato = st.date_input("Fecha de finalización del contrato", value=date.today())
        ajuste_manual = st.number_input("Ajuste manual (opcional)", value=0.0, format="%.2f")
        enviar_liq = st.form_submit_button("Calcular Liquidación")

    if enviar_liq:
        meses_trabajados = calcular_meses(fecha_inicio_contrato, fecha_fin_contrato)
        liquidacion = meses_trabajados * salario + ajuste_manual

        st.success(f"Liquidación calculada: {liquidacion:.2f}")
        
        datos_reporte = {
            "Tipo de contrato": [tipo_contrato],
            "Fecha inicio": [fecha_inicio_contrato],
            "Fecha finalización": [fecha_fin_contrato],
            "Meses trabajados": [meses_trabajados],
            "Salario mensual": [salario],
            "Ajuste manual": [ajuste_manual],
            "Liquidación": [liquidacion]
        }
        df_reporte = pd.DataFrame(datos_reporte)
        st.subheader("Reporte de Liquidación")
        st.dataframe(df_reporte)

        csv = df_reporte.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar reporte en CSV",
            data=csv,
            file_name="reporte_liquidacion.csv",
            mime="text/csv"
        )
