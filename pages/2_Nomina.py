import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.store import employees, transaction_movement as tm
import smtplib
from utils.env import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Inicializar lista de contratos en session_state
if 'contracts' not in st.session_state:
    st.session_state.contracts = []

# Función para calcular meses trabajados
def calcular_meses(inicio, fin):
    return (fin.year - inicio.year) * 12 + (fin.month - inicio.month)

# Función para enviar correo electrónico
def enviar_correo(destinatario, asunto, cuerpo):
    remitente = config['EMAIL_CREDENTIAL'] # Cambiar por el correo de la empresa
    passwd = config['PASSWORD_CREDENTIAL']  # Cambiar por la contraseña del correo

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)  # Cambiar según el proveedor de correo
        servidor.starttls()
        servidor.login(remitente, passwd)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        st.success("Correo enviado exitosamente.")
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Selecciona una sección", ("Administrar Contratos", "Calcular Liquidaciones", "Pagar Nómina"))

if pagina == "Administrar Contratos":
    st.title("Administrar Contratos")
    st.subheader("Registrar un nuevo contrato")
    selected_employee_data = None
    # Seleccionar empleado existente o añadir uno nuevo
    opcion_empleado = st.radio("Seleccione una opción", ("Usar empleado existente", "Registrar nuevo empleado"))

    if opcion_empleado == "Usar empleado existente":
        # Seleccionar empleado existente
        employee_options = [f"{row['name']} ({row['contact']})" for _, row in employees.iterrows()]
        selected_employee = st.selectbox("Seleccionar empleado", options=employee_options)

        # Obtener detalles del empleado seleccionado
        selected_name, selected_contact = selected_employee.split(" (")
        selected_contact = selected_contact[:-1]  # Remover el paréntesis final
        selected_employee_data = employees[(employees['name'] == selected_name) & (employees['contact'] == selected_contact)].iloc[0]

    else:
        # Formulario para registrar nuevo empleado
        st.subheader("Registrar nuevo empleado")
        nombre = st.text_input("Nombre completo")
        contacto = st.text_input("Número de contacto")
        rol = st.selectbox("Rol", options=["Manager", "Accountant", "Engineer", "Supervisor", "Technician", "Analyst"])
        salario_mensual = st.number_input("Salario mensual", min_value=0.0, format="%.2f")
        fecha_ingreso = st.date_input("Fecha de ingreso", value=date.today())
        tipo_contrato = st.selectbox("Tipo de contrato", options=["Permanent", "Temporary"])
        departamento = st.selectbox("Departamento", options=["Finance", "Engineering", "Operations", "Analytics"])
        estado = st.selectbox("Estado", options=["Active", "Inactive"])

        if st.button("Registrar Empleado y Continuar"):
            # Generar un ID único para el empleado
            nuevo_id = f"e{len(employees) + 1}-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
            
            # Crear un nuevo registro de empleado
            nuevo_empleado = {
                'id': nuevo_id,
                'name': nombre,
                'contact': contacto,
                'role': rol,
                'monthly_salary': salario_mensual,
                'entered_date': fecha_ingreso,
                'contract_type': tipo_contrato,
                'end_contract_date': None if tipo_contrato == "Permanent" else fecha_ingreso + timedelta(days=365),
                'department': departamento,
                'status': estado
            }
            
            # Añadir el nuevo empleado al DataFrame
            employees.loc[nuevo_id] = nuevo_empleado
            st.success(f"Empleado {nombre} registrado exitosamente con ID: {nuevo_id}")
            selected_employee_data = employees.loc[nuevo_id]

    # Formulario para registrar contrato
    if selected_employee_data is not None:
        with st.form("form_contrato", clear_on_submit=True):
            tipo_contrato = st.selectbox("Tipo de contrato", options=["Empleado", "Proveedor", "Colaborador", "Otro"])
            fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
            duracion_dias = st.number_input("Duración del contrato (días)", min_value=1, value=30)
            monto = st.number_input("Monto / Salario", min_value=0.0, value=float(selected_employee_data['monthly_salary']), format="%.2f")
            contrato_file = st.file_uploader("Adjuntar contrato (PDF/Imagen)", type=["pdf", "png", "jpg", "jpeg"])
            enviar = st.form_submit_button("Registrar contrato")

        if enviar:
            fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
            nuevo_contrato = {
                "Nombre": selected_employee_data['name'],
                "Contacto": selected_employee_data['contact'],
                "Tipo": tipo_contrato,
                "Fecha inicio": fecha_inicio,
                "Fecha fin": fecha_fin,
                "Monto": monto,
                "Archivo": contrato_file.name if contrato_file else "No adjunto"
            }
            st.session_state.contracts.append(nuevo_contrato)
            st.success("Contrato registrado exitosamente.")

    # Mostrar listado de contratos
    st.subheader("Listado de Contratos")
    if st.session_state.contracts:
        df_contratos = pd.DataFrame(st.session_state.contracts)
        st.dataframe(df_contratos)

        # Alertas para contratos próximos a vencer
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

    # Seleccionar empleado
    employee_options = [f"{row['name']} ({row['contact']})" for _, row in employees.iterrows()]
    selected_employee = st.selectbox("Seleccionar empleado", options=employee_options)

    # Obtener detalles del empleado seleccionado
    selected_name, selected_contact = selected_employee.split(" (")
    selected_contact = selected_contact[:-1]  # Remover el paréntesis final
    selected_employee_data = employees[(employees['name'] == selected_name) & (employees['contact'] == selected_contact)].iloc[0]

    # Formulario para calcular liquidación
    with st.form("form_liquidacion", clear_on_submit=True):
        tipo_contrato = st.selectbox("Tipo de contrato", options=["Empleado", "Colaborador", "Otro"])
        salario = st.number_input("Salario / Monto mensual", min_value=0.0, value=float(selected_employee_data['monthly_salary']), format="%.2f")
        fecha_inicio_contrato = st.date_input("Fecha de inicio del contrato", value=selected_employee_data['entered_date'].to_pydatetime().date())
        fecha_fin_contrato = st.date_input("Fecha de finalización del contrato", value=date.today())
        ajuste_manual = st.number_input("Ajuste manual (opcional)", value=0.0, format="%.2f")
        enviar_liq = st.form_submit_button("Calcular Liquidación")

    if enviar_liq:
        meses_trabajados = calcular_meses(fecha_inicio_contrato, fecha_fin_contrato)
        liquidacion = meses_trabajados * salario + ajuste_manual

        st.success(f"Liquidación calculada: {liquidacion:.2f}")
        
        # Crear reporte de liquidación
        datos_reporte = {
            "Nombre": [selected_name],
            "Contacto": [selected_contact],
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

        # Botón para descargar reporte en CSV
        csv = df_reporte.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar reporte en CSV",
            data=csv,
            file_name="reporte_liquidacion.csv",
            mime="text/csv"
        )

elif pagina == "Pagar Nómina":
    st.title("Pagar Nómina")
    st.subheader("Realizar el pago de nómina a un empleado")

    # Seleccionar empleado
    employee_options = [f"{row['name']} ({row['contact']})" for _, row in employees.iterrows()]
    selected_employee = st.selectbox("Seleccionar empleado", options=employee_options)

    # Obtener detalles del empleado seleccionado
    selected_name, selected_contact = selected_employee.split(" (")
    selected_contact = selected_contact[:-1]  # Remover el paréntesis final
    selected_employee_data = employees[(employees['name'] == selected_name) & (employees['contact'] == selected_contact)].iloc[0]

    # Formulario para pagar nómina
    
    st.write("### Detalles del Pago")
    salario_base = st.number_input("Salario base", min_value=0.0, value=float(selected_employee_data['monthly_salary']), format="%.2f", step=100.0)
    
    # Initialize session state for tiene_horas_extras if it doesn't exist
    if 'tiene_horas_extras' not in st.session_state:
        st.session_state.tiene_horas_extras = False
    
    # Update session state based on checkbox value
    st.session_state.tiene_horas_extras = st.checkbox("Tiene horas extras", value=st.session_state.tiene_horas_extras)
    
    # Enable/disable horas_extras based on checkbox value
    horas_extras = st.number_input(
        "Horas extras trabajadas", 
        min_value=0, 
        value=0, 
        disabled=not st.session_state.tiene_horas_extras,
    )
    
    valor_hora_extra = selected_employee_data['overtime_rate']
    monto_horas_extras = horas_extras * valor_hora_extra if st.session_state.tiene_horas_extras else 0.0
    monto_total = salario_base + monto_horas_extras

    st.write(f"**Monto total a pagar:** ${monto_total:,.2f}")

    enviar_pago = st.button("Realizar Pago")

    if enviar_pago:
        # Guardar la transacción
        nueva_transaccion = {
            'id': str(len(tm) + 1),
            'work_id': None,  # No asociado a una obra
            'description': f"Pago de nómina a {selected_name}",
            'category': 'nomina',
            'date': pd.Timestamp.now(),
            'end_date': None,
            'transaction_type': 'expense',
            'amount': monto_total,
            'stabilization_fund_percentage': 0.0,
            'subject': selected_name
        }
        tm.loc[len(tm)] = nueva_transaccion

        # Enviar correo electrónico al empleado
        asunto = f"Factura de Pago de Nómina - {selected_name}"
        cuerpo = f"""
        Estimado/a {selected_name},

        Se ha realizado el pago de su nómina con los siguientes detalles:
        - Salario base: ${salario_base:,.2f}
        - Horas extras: {horas_extras} horas (${monto_horas_extras:,.2f})
        - Monto total: ${monto_total:,.2f}

        Gracias por su trabajo.
        """
        enviar_correo(selected_employee_data['email'], asunto, cuerpo)

        st.success(f"Pago de ${monto_total:,.2f} realizado exitosamente. Se ha enviado un correo a {selected_name}.")