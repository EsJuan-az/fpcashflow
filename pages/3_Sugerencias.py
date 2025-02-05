import streamlit as st
import pandas as pd
from utils.auth0 import getAuth0
import base64
from utils.store import transaction_movement as tm
import time
import numpy as np


st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

user_info = getAuth0()
if user_info:
    st.title("_SUGERENCIAS DE_ :green[PORCENTAJE]")
    
    col1, col2, col3 = st.columns(3)
    income = tm[tm['transaction_type'] == 'income']['amount'].sum()
    expense = tm[tm['transaction_type'] == 'expense']['amount'].sum()
    balance = income - expense

    sum_income=(1/100)*(tm[tm['transaction_type'] == 'income']['amount']* tm[tm['transaction_type'] == 'income']['stabilization_fund_percentage']).sum()
    sum_expense=(1/100)*(tm[tm['transaction_type'] == 'expense']['amount']* tm[tm['transaction_type'] == 'expense']['stabilization_fund_percentage']).sum()
    
    balance_fund=sum_income-sum_expense
    value2 = balance * 0.20
    
    col1.metric(label="Deficit total proyectado", value=f"${balance:,.0f}")
    col2.metric(label="Margen de seguridad", value=f"${value2:,.0f}")
    
    suma = balance + value2
    col3.metric(label="Balance", value=f"${suma:,.0f}")

    
    _PARRAFO1 = """
    Diagnóstico exhaustivo: Identifica las causas del balance negativo. ¿Son gastos excesivos, ingresos insuficientes, deudas acumuladas, malas inversiones o una combinación de factores?
    Evaluación de activos: Determina qué activos se pueden vender rápidamente para generar efectivo (inventario, equipos, propiedades).
    Análisis de deudas: Clasifica las deudas por tipo (bancarias, proveedores, etc.), tasas de interés y plazos.
    Flujo de caja: Elabora una proyección detallada de ingresos y gastos para los próximos meses.
    """
    
    _PARRAFO2 = """
    REDUCCION URGENTE DE GASTOS
    Gastos esenciales vs. no esenciales: Elimina o reduce drásticamente los gastos no esenciales (publicidad, viajes, representación).
Renegociación de contratos: Busca mejores condiciones con proveedores, arrendadores y prestamistas.
Congelación de contrataciones: Evita nuevas contrataciones y considera reducir personal si es necesario.
Externalización de servicios: Evalúa si es más rentable subcontratar ciertas actividades (contabilidad, limpieza, etc.)."""

    _PARRAFO3 = """
    AUMENTO DE INGRESOS
    Ventas: Implementa estrategias agresivas para aumentar las ventas (descuentos, promociones, publicidad).
Nuevos mercados: Explora nuevos nichos de mercado o canales de distribución.
Productos/servicios: Considera ampliar tu oferta con productos o servicios complementarios.
Aumento de precios: Si es posible, ajusta los precios para mejorar los márgenes de ganancia."""

    _PARRAFO4 = """
    Investigación y análisis: Antes de invertir, investiga a fondo las diferentes opciones disponibles (acciones, bonos, bienes raíces, etc.) y evalúa los riesgos y rendimientos potenciales.
Diversificación: No pongas todos tus huevos en la misma canasta. Diversifica tus inversiones para reducir el riesgo.
Horizonte de inversión: Define tus objetivos de inversión a largo plazo y ajusta tu estrategia en consecuencia.
Asesoramiento profesional: Si no estás seguro de cómo invertir, busca el asesoramiento de un experto financiero.
    """
    _PARRAFO5 = """
    Expansión del mercado: Explora nuevos mercados o nichos para aumentar tus ventas y base de clientes.
Desarrollo de nuevos productos/servicios: Invierte en investigación y desarrollo para innovar y mantener tu oferta actualizada.
Mejora de la eficiencia: Identifica áreas donde puedas optimizar procesos y reducir costos sin sacrificar la calidad.
Adquisiciones estratégicas: Considera la posibilidad de adquirir otras empresas para expandir tu negocio y ganar cuota de mercado.
    
    """
    
    _PARRAFO6 = """
    Planificación financiera: Elabora un plan financiero detallado que incluya proyecciones de ingresos, gastos y flujo de caja.
Control presupuestario: Monitorea tus ingresos y gastos de cerca para asegurarte de que estás cumpliendo con tu presupuesto.
Análisis de rentabilidad: Evalúa la rentabilidad de cada producto o servicio para identificar áreas de mejora.
Gestión de riesgos: Identifica los riesgos financieros que enfrenta tu empresa y toma medidas para mitigarlos.
    
    """



def stream_data(n):
    if n == 1:
        st.header("_ANALISIS_ :green[PROFUNDO Y REALISTA:] ", divider = "red")
        for word in _PARRAFO1.split(" "):
            yield word + " "
            time.sleep(0.02)

        for word in _PARRAFO2.split(" "):
            yield word + " "
            time.sleep(0.02)
            
        for word in _PARRAFO3.split(" "):
            yield word + " "
            time.sleep(0.02)
            
    else:
        st.header("_INVERSION_ :green[INTELIGENTE:] ", divider = "green")
        for word in _PARRAFO4.split(" "):
            yield word + " "
            time.sleep(0.02)
            
        for word in _PARRAFO5.split(" "):
            yield word + " "
            time.sleep(0.01)
            
        for word in _PARRAFO6.split(" "):
            
            yield word + " "
            time.sleep(0.02)
            
            
columna1, columna2, columna3 = st.columns(3)
CO1, CO2, CO3 = st.columns(3)

CO1.title(":red[GASTOS]")

c01, c02, c03 = st.columns(3)
gastos = tm[tm['transaction_type'] == 'expense']['amount'].sum()
gastosPromedio =tm[tm['transaction_type'] == 'expense']['amount'].mean().__round__(2)
cantidadGastos = tm[tm['transaction_type'] == 'expense']['amount'].count()
calculoDesviacionGastos=((((tm[tm['transaction_type'] == 'expense']['amount'] - gastosPromedio) ** 2).sum()) // (cantidadGastos - 1))  ** 0.5

st.title(":green[INGRESOS]")
c01.metric(label="Promedio", value=f"${gastosPromedio}", delta=f"${gastos/100:.0f}")
c02.metric(label="Total", value=f"${gastos:,.0f}")
c03.metric(label="Desviación", value=f"${calculoDesviacionGastos:.0f}")



c04, c05, c06 = st.columns(3)
ingresos = tm[tm['transaction_type'] == 'income']['amount'].sum()
ingresosPromedio =tm[tm['transaction_type'] == 'income']['amount'].mean().__round__(2)
cantidadIngresos = tm[tm['transaction_type'] == 'income']['amount'].count()
calculoDesviacionIngresos=((((tm[tm['transaction_type'] == 'income']['amount'] - ingresosPromedio) ** 2).sum()) // (cantidadIngresos - 1))  ** 0.5

c04.metric(label="Promedio", value=f"${ingresosPromedio}", delta=f"${ingresos/100:.0f}")
c05.metric(label="Total", value=f"${ingresos:,.0f}")
c06.metric(label="Desviación", value=f"${calculoDesviacionIngresos:.0f}")

factorSeguridad = (tm[tm['transaction_type'] == 'expense']['amount']* tm[tm['transaction_type'] == 'expense']['stabilization_fund_percentage']).mean()
fondo = 6 *(gastosPromedio + calculoDesviacionGastos * 0.3)

st.markdown(f"<div style='text-align: center; font-size: 40px; color: yellow;'>{"FONDO DE ESTABILIZACIÓN"}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; font-size: 40px;'>${fondo:.0f}</div>", unsafe_allow_html=True)

if balance < 0:
        st.divider()
        st.title("_Balance negativo_")
        st.subheader("Se recomienda seguir los siguientes pasos: ")  
         
        if st.button("mostar sugerencias", type= "secondary"):
            st.write_stream(stream_data(1))
        st.divider()
            
else:
        st.divider()
        st.title("_Balance positivo_")
        
        st.subheader("Se recomienda seguir los siguientes pasos: ")
        
        if st.button("mostar sugerencias", type= "secondary"):  
            st.write_stream(stream_data(0))
        
        st.divider()
     
        