import streamlit as st
import pandas as pd

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

data = {
    "#": [1, 2, 3, 4, 5],
    "Proyecto": ["Aire Campestre", "Aire Campestre", "Plaza Belverde", "Plaza Belverde", "Aire Campestre"],
    "Factura": ["RNVB-012", "SDA-432", "DAS-032", "MCD-980", "WQE-112"],
    "% Pago Factura": [15, 20, 50, 40, 50],
    "Monto a consignar": [80000, 120000, 90000, 60000, 50000],
    "Proveedor": ["Aire Verde", "ConstruLAB", "Universidad Nacional", "FimaTech", "Consultores & Asociados RBA"],
    "Descripción": ["Aires acondicionados del nivel 12", "Análisis de suelos de torre 1", "Patología y muestras de suelo", 
                    "Revisión Computadores", "Asesoría demanda por daños"],
    "Fecha de vencimiento": pd.to_datetime(["2025-02-05", "2025-02-03", "2025-02-06", "2025-02-02", "2025-02-04"]),
}

df = pd.DataFrame(data)
df_sorted = df.sort_values(by="Fecha de vencimiento")

opciones_proyecto = df["Proyecto"].unique()
opciones_proveedor = df["Proveedor"].unique()

tab1, tab2, tab3 = st.tabs(["📊 Flujo de Caja", "➕ Registrar Gasto", "💰 Pagar Facturas"])

with tab1:
    st.subheader("🔍 Gastos con vencimiento más próximo")    
    st.dataframe(df_sorted, hide_index=True)

with tab2:
    st.subheader("➕ Registrar pago inesperado")

    with st.form("form_registro"):
        proyecto = st.selectbox("Selecciona el Proyecto", opciones_proyecto)
        factura = st.text_input("Número de Factura", placeholder="Ej: ABC-123")
        pago_factura = st.slider("Porcentaje de Pago de la Factura (%)", min_value=0, max_value=100, step=5)
        monto = st.number_input("Monto a consignar", min_value=10000, step=10000, format="%.0f")
        proveedor = st.selectbox("Proveedor", opciones_proveedor)
        descripcion = st.text_area("Descripción", placeholder="Ej: Compra de material")
        fecha_vencimiento = st.date_input("Fecha de vencimiento")
        
        submitted = st.form_submit_button("Guardar")
        if submitted:
            st.success(f"Gasto registrado en {proyecto} - Factura {factura} - {pago_factura}% de pago - ${monto} - {proveedor} - {descripcion} - Vence el {fecha_vencimiento}")

with tab3:
    st.subheader("💰 Seleccionar facturas a pagar")
    
    facturas_a_pagar = []
    for index, row in df_sorted.iterrows():
        pagar = st.checkbox(f"Factura {row['Factura']} - ${row['Monto a consignar']} - {row['Proveedor']}", key=row['Factura'])
        if pagar:
            facturas_a_pagar.append(row)

    if st.button("✅ Pagar Seleccionadas"):
        if facturas_a_pagar:
            st.success("✅ Se han pagado las siguientes facturas:")
            for factura in facturas_a_pagar:
                st.write(f"✔️ {factura['Factura']} - ${factura['Monto a consignar']} - {factura['Proveedor']}")
        else:
            st.warning("⚠️ No se seleccionó ninguna factura para pagar.")
