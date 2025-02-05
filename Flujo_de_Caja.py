import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from utils.auth0 import getAuth0
from utils.store import transaction_movement as tm
import time
import numpy as np


st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

user_info = getAuth0()
if user_info:
    st.write("### Cash Flow")
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    income = tm[tm['transaction_type'] == 'income']['amount'].sum()
    expense = tm[tm['transaction_type'] == 'expense']['amount'].sum()
    balance = income - expense
    col1.metric(label="Ingresos", value=f"${income:,.0f}")
    col2.metric(label="Balance", value=f"${balance:,.0f}")
    col3.metric(label="Egresos", value=f"${expense:,.0f}")

    sf_sum_income=(1/100)*(tm[tm['transaction_type'] == 'income']['amount']* tm[tm['transaction_type'] == 'income']['stabilization_fund_percentage']).sum()
    sf_sum_expense=(1/100)*(tm[tm['transaction_type'] == 'expense']['amount']* tm[tm['transaction_type'] == 'expense']['stabilization_fund_percentage']).sum()
    
    balance_fund=sf_sum_income-sf_sum_expense
    balance_free = balance - balance_fund
    col4.metric(label="Balance fondo", value=f"${balance_fund:,.0f}")
    col5.metric(label='Balance libre de uso', value=f'${balance_free:,.0f}')


    
    if st.button('Registrar transacción'):
        register_transaction()
    
    with st.container(border=True):
        st.write("#### Gráfica de Ingresos y Egresos")

        tm_incomes = tm.copy()
        tm_incomes = pd.DataFrame(tm_incomes[tm_incomes["transaction_type"] == "income"][["amount", "description", "date", "stabilization_fund_percentage"]])
        tm_incomes.rename(columns={"amount":"Ingreso"}, inplace=True)

        tm_expenses = tm.copy() #9100
        tm_expenses = pd.DataFrame(tm_expenses[tm_expenses["transaction_type"] == "expense"][["amount", "description", "date", "stabilization_fund_percentage"]])
        tm_expenses.rename(columns={"amount":"Gasto"}, inplace=True)
        
        tm_movements_date = pd.merge(tm_incomes[['Ingreso', 'date']], tm_expenses[['Gasto', 'date']], how="outer", on='date')
        st.bar_chart(tm_movements_date, y=["Ingreso", "Gasto"], x="date", x_label="Fecha", y_label="Valor", color=["#ff2c2c", "#3DEC55"])

        st.write("#### Gráfica de movimientos del Fondo de Estabilización")

        fe_incomes = tm_incomes.copy()
        fe_incomes["stabilization_fund_percentage"] = fe_incomes["stabilization_fund_percentage"] / 100
        fe_incomes["Ingreso"] = fe_incomes["Ingreso"] * fe_incomes["stabilization_fund_percentage"]
        
        fe_expenses = tm_expenses.copy()
        fe_expenses["stabilization_fund_percentage"] = fe_expenses["stabilization_fund_percentage"] / 100
        fe_expenses["Gasto"] = fe_expenses["Gasto"] * fe_expenses["stabilization_fund_percentage"]

        fe_movements_date = pd.merge(fe_incomes[['Ingreso', 'date']], fe_expenses[['Gasto', 'date']], how="outer", on='date')
        
        st.bar_chart(fe_movements_date, y=["Ingreso", "Gasto"], x="date", x_label="Fecha", y_label="Valor", color=["#ff2c2c", "#3DEC55"])
else:
    sleep(1)
    st.error('Inicia sesión para continuar.')
