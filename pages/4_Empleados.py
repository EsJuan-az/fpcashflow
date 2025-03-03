import streamlit as st
import pandas as pd
from time import sleep
from datetime import date, timedelta
from utils.store import work as w, employees  # Use `employees` from utils.store
from utils.auth0 import getAuth0 
from ui.modals import register_work
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)


# Sidebar navigation
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Selecciona una sección", ("Añadir Nuevo Empleado", "Actualizar Datos de Empleado"))

if getAuth0():
    if pagina == "Añadir Nuevo Empleado":
        st.title("Añadir Nuevo Empleado")
        st.subheader("Registrar un nuevo empleado en el sistema")

        # Formulario para añadir empleado
        with st.form("form_empleado", clear_on_submit=True):
            nombre = st.text_input("Nombre completo")
            contacto = st.text_input("Número de contacto")
            rol = st.selectbox("Rol", options=["Manager", "Accountant", "Engineer", "Supervisor", "Technician", "Analyst"])
            salario_mensual = st.number_input("Salario mensual", min_value=0.0, format="%.2f")
            fecha_ingreso = st.date_input("Fecha de ingreso", value=date.today())
            tipo_contrato = st.selectbox("Tipo de contrato", options=["Permanent", "Temporary"])
            departamento = st.selectbox("Departamento", options=["Finance", "Engineering", "Operations", "Analytics"])
            estado = st.selectbox("Estado", options=["Active", "Inactive"])

            # Nuevos campos con valores predeterminados
            aportes_pension = st.number_input("Aportes pensión (%)", min_value=0.0, max_value=100.0, value=4.0, format="%.2f")
            cesantias = st.number_input("Cesantías (%)", min_value=0.0, max_value=100.0, value=8.33, format="%.2f")
            prima = st.number_input("Prima (%)", min_value=0.0, max_value=100.0, value=8.33, format="%.2f")
            valor_hora_extra = st.number_input("Valor hora extra", min_value=0.0, value=20.0, format="%.2f")

            enviar_empleado = st.form_submit_button("Registrar Empleado")

        if enviar_empleado:
            # Generar un ID único para el empleado
            nuevo_id = f"e{len(employees) + 1}-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
            
            # Crear un nuevo registro de empleado
            nuevo_empleado = {
                'id': nuevo_id,
                'name': nombre,
                'contact': contacto,
                'role': rol,
                'monthly_salary': float(salario_mensual),  # Ensure float type
                'entered_date': fecha_ingreso,
                'contract_type': tipo_contrato,
                'end_contract_date': None if tipo_contrato == "Permanent" else fecha_ingreso + timedelta(days=365),
                'department': departamento,
                'status': estado,
                'pension_contributions': aportes_pension / 100,  # Convertir porcentaje a decimal
                'severance': cesantias / 100,  # Convertir porcentaje a decimal
                'bonus': prima / 100,  # Convertir porcentaje a decimal
                'overtime_rate': valor_hora_extra
            }
            
            # Añadir el nuevo empleado al DataFrame
            employees.loc[len(employees)] = nuevo_empleado
            st.success(f"Empleado {nombre} registrado exitosamente con ID: {nuevo_id}")

    elif pagina == "Actualizar Datos de Empleado":
        st.title("Actualizar Datos de Empleado")
        st.subheader("Selecciona un empleado para actualizar sus datos")

        # Selector de empleado
        employee_options = [f"{row['name']} ({row['contact']})" for _, row in employees.iterrows()]
        selected_employee = st.selectbox("Seleccionar empleado", options=employee_options)

        # Obtener los datos del empleado seleccionado
        selected_name, selected_contact = selected_employee.split(" (")
        selected_contact = selected_contact[:-1]  # Remover el paréntesis final
        selected_employee_data = employees[(employees['name'] == selected_name) & (employees['contact'] == selected_contact)].iloc[0]

        # Formulario para actualizar datos
        with st.form("form_actualizar_empleado"):
            st.write("### Datos del Empleado")
            nombre = st.text_input("Nombre completo", value=selected_employee_data['name'])
            contacto = st.text_input("Número de contacto", value=selected_employee_data['contact'])
            rol = st.selectbox("Rol", options=["Manager", "Accountant", "Engineer", "Supervisor", "Technician", "Analyst"], index=["Manager", "Accountant", "Engineer", "Supervisor", "Technician", "Analyst"].index(selected_employee_data['role']))
            salario_mensual = st.number_input("Salario mensual", min_value=0.0, value=float(selected_employee_data['monthly_salary']), format="%.2f")  # Ensure float type
            fecha_ingreso = st.date_input("Fecha de ingreso", value=selected_employee_data['entered_date'])
            tipo_contrato = st.selectbox("Tipo de contrato", options=["Permanent", "Temporary"], index=["Permanent", "Temporary"].index(selected_employee_data['contract_type']))
            departamento = st.selectbox("Departamento", options=["Finance", "Engineering", "Operations", "Analytics"], index=["Finance", "Engineering", "Operations", "Analytics"].index(selected_employee_data['department']))
            estado = st.selectbox("Estado", options=["Active", "Inactive"], index=["Active", "Inactive"].index(selected_employee_data['status']))

            # Nuevos campos con valores actuales
            aportes_pension = st.number_input("Aportes pensión (%)", min_value=0.0, max_value=100.0, value=selected_employee_data['pension_contributions'] * 100, format="%.2f")
            cesantias = st.number_input("Cesantías (%)", min_value=0.0, max_value=100.0, value=selected_employee_data['severance'] * 100, format="%.2f")
            prima = st.number_input("Prima (%)", min_value=0.0, max_value=100.0, value=selected_employee_data['bonus'] * 100, format="%.2f")
            valor_hora_extra = st.number_input("Valor hora extra", min_value=0.0, value=selected_employee_data['overtime_rate'], format="%.2f")

            guardar_cambios = st.form_submit_button("Guardar Cambios")

        if guardar_cambios:
            # Actualizar los datos del empleado
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'name'] = nombre
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'contact'] = contacto
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'role'] = rol
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'monthly_salary'] = float(salario_mensual)  # Ensure float type
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'entered_date'] = fecha_ingreso
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'contract_type'] = tipo_contrato
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'department'] = departamento
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'status'] = estado
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'pension_contributions'] = aportes_pension / 100
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'severance'] = cesantias / 100
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'bonus'] = prima / 100
            employees.loc[(employees['name'] == selected_name) & (employees['contact'] == selected_contact), 'overtime_rate'] = valor_hora_extra

            st.success(f"Datos de {nombre} actualizados exitosamente.")
else:
    sleep(1)
    st.error('Inicia sesión para continuar.')