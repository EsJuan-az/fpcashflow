import streamlit as st
import pandas as pd
from utils.store import transaction_movement as tm

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
tab1.subheader("Subtitulo del tab 1")
tab2.subheader("Subtitulo del tab 2")

with tab1:
  with st.popover("Registrar transaccion", use_container_width=True):
    with st.form("formulario1"):
      entry_1 = st.text_input("Dato 1", placeholder="Ingrese el dato...")
      submitted = st.form_submit_button("Aceptar")
      if submitted:
        st.write("Dato ingresado:", entry_1)
    
  st.write("## Gráfica de ingresos y egresos")
  tm_incomes = tm.copy()
  tm_incomes = pd.DataFrame(tm_incomes[tm_incomes["transaction_type"] == "income"][["amount", "description", "date", "stabilization_fund_percentage"]])
  tm_incomes.rename(columns={"amount":"Ingreso"}, inplace=True)

  tm_expenses = tm.copy()
  tm_expenses = pd.DataFrame(tm_expenses[tm_expenses["transaction_type"] == "expense"][["amount", "description", "date", "stabilization_fund_percentage"]])
  tm_expenses.rename(columns={"amount":"Gasto"}, inplace=True)
  tm_movements_date = pd.merge(tm_incomes[['Ingreso', 'date']], tm_expenses[['Gasto', 'date']], how="outer", on='date')
  
  st.bar_chart(tm_movements_date, y=["Ingreso", "Gasto"], x="date", x_label="Fecha", y_label="Valor", color=["#ff2c2c", "#3DEC55"])

with tab2:
  with st.popover("Registrar transaccion"):
    with st.form("formulario2"):
      entry_2 = st.text_input("Dato 2", placeholder="Ingrese el dato...")  
      submitted = st.form_submit_button("Aceptar")
      if submitted:
        st.write("Dato ingresado:", entry_2)
  
  st.write("## Gráfica de movimientos del fondo de estabilización")
  fe_incomes = tm_incomes.copy()
  fe_incomes["stabilization_fund_percentage"] = fe_incomes["stabilization_fund_percentage"] / 100
  fe_incomes["Ingreso"] = fe_incomes["Ingreso"] * fe_incomes["stabilization_fund_percentage"]
  
  fe_expenses = tm_expenses.copy()
  fe_expenses["stabilization_fund_percentage"] = fe_expenses["stabilization_fund_percentage"] / 100
  fe_expenses["Gasto"] = fe_expenses["Gasto"] * fe_expenses["stabilization_fund_percentage"]

  fe_movements_date = pd.merge(fe_incomes[['Ingreso', 'date']], fe_expenses[['Gasto', 'date']], how="outer", on='date')
  
  st.bar_chart(fe_movements_date, y=["Ingreso", "Gasto"], x="date", x_label="Fecha", y_label="Valor", color=["#ff2c2c", "#3DEC55"])