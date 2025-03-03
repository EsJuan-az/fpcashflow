import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from utils.auth0 import getAuth0
from utils.store import transaction_movement as tm, work, suppliers, products, employees
from ui.modals import register_transaction
from utils.data import stabilization_fund_historic, required_for_stabilization_historic, pending_expenses
from io import BytesIO

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

user_info = getAuth0()
if user_info:
    st.write("# Flujo de Caja")
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    income = tm[tm['transaction_type'] == 'income']['amount'].sum()
    expense = tm[tm['transaction_type'] == 'expense']['amount'].sum()
    balance = income - expense
    col1.metric(label="Ingresos", value=f"${income:,.0f}")
    col2.metric(label="Balance", value=f"${balance:,.0f}")
    col3.metric(label="Egresos", value=f"${expense:,.0f}")

    sf_sum_income = (1 / 100) * (tm[tm['transaction_type'] == 'income']['amount'] * tm[tm['transaction_type'] == 'income']['stabilization_fund_percentage']).sum()
    sf_sum_expense = (1 / 100) * (tm[tm['transaction_type'] == 'expense']['amount'] * tm[tm['transaction_type'] == 'expense']['stabilization_fund_percentage']).sum()
    balance_fund = sf_sum_income - sf_sum_expense
    balance_free = balance - balance_fund
    col4.metric(label="Balance fondo", value=f"${balance_fund:,.0f}")
    col5.metric(label='Balance libre de uso', value=f'${balance_free:,.0f}')

    if st.button('Registrar transacción'):
        register_transaction()

    # Botón para generar informe
    if st.button('Generar informe'):
        # Calcular métricas financieras
        total_transactions = len(tm)
        avg_transaction = tm['amount'].mean()
        gross_profit_margin = (income - expense) / income if income != 0 else 0
        net_profit_margin = balance / income if income != 0 else 0
        cash_flow = income - expense
        liquidity_ratio = income / expense if expense != 0 else 0
        cash_days = (balance / expense * 30) if expense != 0 else 0  # Días de efectivo disponible
        income_growth_rate = (tm[tm['transaction_type'] == 'income']['amount'].pct_change().mean()) * 100
        expense_growth_rate = (tm[tm['transaction_type'] == 'expense']['amount'].pct_change().mean()) * 100

        # Rentabilidad por obra
        work_profitability = tm.groupby('work_id')['amount'].sum().reset_index()
        work_profitability = work_profitability.merge(work, left_on='work_id', right_index=True)
        work_profitability['profitability'] = work_profitability['amount'] / work_profitability['stipulated_payment']

        # Valor del Tiempo de Vida del Cliente (LTV) y Costo de Adquisición de Cliente (CAC)
        ltv = income / len(tm[tm['transaction_type'] == 'income']) if len(tm[tm['transaction_type'] == 'income']) != 0 else 0
        cac = expense / len(tm[tm['transaction_type'] == 'income']) if len(tm[tm['transaction_type'] == 'income']) != 0 else 0

        # Crear un DataFrame con las métricas
        metrics_df = pd.DataFrame({
            'Métrica': [
                'Ingresos Totales', 'Gastos Totales', 'Balance Neto', 'Número de Transacciones',
                'Promedio de Transacción', 'Margen de Ganancia Bruta', 'Margen de Beneficio Neto',
                'Flujo de Caja Neto', 'Ratio de Liquidez', 'Días de Efectivo Disponible',
                'Tasa de Crecimiento de Ingresos', 'Tasa de Crecimiento de Gastos',
                'Valor del Tiempo de Vida del Cliente (LTV)', 'Costo de Adquisición de Cliente (CAC)'
            ],
            'Valor': [
                income, expense, balance, total_transactions, avg_transaction,
                gross_profit_margin, net_profit_margin, cash_flow, liquidity_ratio,
                cash_days, income_growth_rate, expense_growth_rate, ltv, cac
            ]
        })

        # Rentabilidad por obra
        work_metrics_df = work_profitability[['name', 'profitability']].rename(columns={'name': 'Obra', 'profitability': 'Rentabilidad'})

        # Crear un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            metrics_df.to_excel(writer, sheet_name='Métricas Generales', index=False)
            work_metrics_df.to_excel(writer, sheet_name='Rentabilidad por Obra', index=False)
        
        output.seek(0)

        # Descargar el archivo Excel
        st.download_button(
            label="Descargar informe en Excel",
            data=output,
            file_name="informe_financiero.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    col1, col2 = st.columns(2)

    with col1:
        pe = pending_expenses()
        total_pagos = len(pe)
        monto_total = pe["amount"].sum()

        st.markdown("---")  
        st.markdown("<h2 style='text-align: center;'>💰 Estado de Pagos</h2>", unsafe_allow_html=True)
        msg1 = '✅ No hay pagos pendientes'
        msg2 = 'Todo está al día'
        if total_pagos > 0:
            msg1 = f'🔴 Hay {total_pagos} pagos pendientes'
            msg2 = f'Total a pagar: ${monto_total:,.0f}'
            
        st.markdown(f"""
        <div style="padding:15px; border-radius:10px; text-align:center; border: 1px solid white;">
            <h3 style="color:white;">{msg1}</h3>
            <p style="color:white; font-size:18px;"><strong>{msg2}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")  

        st.subheader("🔍 Gastos con próximo vencimiento")
        present_df = pe.copy()
        present_df = present_df.rename({'description': 'Descripción', 'amount': 'Monto', 'name': 'Obra'}, axis=1)
        st.dataframe(present_df[["Obra","Descripción", "Monto"]], hide_index=True)

    with col2:
        st.write("#### Gráfica de Ingresos y Egresos")

        tm_incomes = tm.copy()
        tm_incomes = pd.DataFrame(tm_incomes[tm_incomes["transaction_type"] == "income"][["amount", "description", "date", "stabilization_fund_percentage"]])
        tm_incomes.rename(columns={"amount":"Ingreso"}, inplace=True)

        tm_expenses = tm.copy()
        tm_expenses = pd.DataFrame(tm_expenses[tm_expenses["transaction_type"] == "expense"][["amount", "description", "date", "stabilization_fund_percentage"]])
        tm_expenses.rename(columns={"amount":"Gasto"}, inplace=True)
        
        tm_movements_date = pd.merge(tm_incomes[['Ingreso', 'date']], tm_expenses[['Gasto', 'date']], how="outer", on='date')
        st.bar_chart(tm_movements_date, y=["Ingreso", "Gasto"], x="date", x_label="Fecha", y_label="Valor", color=["#ff2c2c", "#3DEC55"])

        st.write("#### Gráfica de movimientos del Fondo de Estabilización")

        sf_historic = stabilization_fund_historic()
        sf_required = required_for_stabilization_historic()

        fe_incomes = tm_incomes.copy()
        fe_incomes["Ingreso"] = fe_incomes["Ingreso"] * fe_incomes["stabilization_fund_percentage"] / 100
        
        fe_expenses = tm_expenses.copy()
        fe_expenses["Gasto"] = fe_expenses["Gasto"] * fe_expenses["stabilization_fund_percentage"] / 100

        fe_movements_date = pd.merge(fe_incomes[['Ingreso', 'date']], fe_expenses[['Gasto', 'date']], how="outer", on='date')

        sf_movements_date = pd.concat([sf_required, sf_historic], axis=1)
        st.area_chart(
            sf_movements_date.rename(
                mapper={
                    'stabilization_fund_amount': 'Cantidad en el Fondo',
                    'required_stabilization_fund': 'Cantidad requerida en fondo'
                },
                axis=1
            ),
            color=('#AF1B3F', '#29274C'),
            y_label='Cantidad de Dinero'
        )
else:
    sleep(1)
    st.error('Inicia sesión para continuar.')