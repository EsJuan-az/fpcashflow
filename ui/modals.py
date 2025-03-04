import streamlit as st
import pandas as pd
from uuid import uuid4
from utils.store import work as w, transaction_movement as tm
from utils.data import recommended_destination_percentage

@st.dialog("Registrar nueva obra")
def register_work():
  st.session_state.error_message_2 = None
  name = st.text_input("Nombre:")
  payment = st.number_input('Pago Estipulado:', step=10000)
  st.session_state.error_message_2 = st.session_state.error_message_2 if payment > 0 else 'Pago estipulado debe ser mayor que cero'
  start = st.date_input("Fecha de comienzo:")
  end = st.date_input("Fecha de finalización:")
  if st.session_state.error_message_2:
    st.error(f'### Error\n*{st.session_state.error_message_2}*')
  if st.button("Registrar", disabled=bool(st.session_state.error_message_2)):
    id = str(uuid4())
    w.loc[id] = [name, payment, pd.to_datetime(start), pd.to_datetime(end)]
    st.rerun()


@st.dialog("Registrar nueva transacción")
def register_transaction():  
  st.session_state.error_message = None
  # Description Validation
  description = st.text_input("Asunto:", placeholder="Descripción de la transacción")
  st.session_state.error_message = st.session_state.error_message if len(description.strip()) > 0 else 'La descripción de su transacción es obligatoria.'
  
  # Work Validation
  work_id = st.selectbox('Obra relacionada:', w['name'], index = None, placeholder='Selecciona una obra')
  
  #Movement type validation
  mov_type = st.selectbox('Tipo de movimiento:', ["Gasto", "Ingreso"], index=0, placeholder='Selecciona un tipo de movimiento')
  
  # Subject validation
  subject = st.text_input('Destinatario:' if mov_type == 'Gasto' else 'Origen', placeholder="Nombre de la empresa o persona")
  st.session_state.error_message = st.session_state.error_message if len(subject.strip()) > 0 else 'El sujeto de su movimiento es obligatorio.'
  
  category = st.selectbox("Categoría:", ["Mensual", "Única"], index=1, placeholder='Selecciona una frecuencia')
  amount = st.number_input("Monto total:", step=10000)
  st.session_state.error_message = st.session_state.error_message if amount > 0 else 'El monto debe ser mayor que cero.'
  
  date_transaction = st.date_input("Fecha de transacción:")
  end_transaction = pd.NaT
  
  if category == "Mensual":
    end_transaction = st.date_input("Fecha de finalización:")
    
  stabilization_fund_percentage = 0
  if mov_type == 'Ingreso' and amount > 0:
    recommended = recommended_destination_percentage(amount)
    print(recommended)
    
    st.write("#### Decida cuánto porcentaje de su ingreso irá al fondo")
    stabilization_fund_percentage = st.slider('Porcentaje destinado a fondo de estabilización', 0.0, 100.0, float(recommended))
    st.write(f'##### Recomendado: {recommended}%\n ##### Decisión: {stabilization_fund_percentage}%\n##### Cantidad: ${stabilization_fund_percentage * amount / 100}')
  if st.session_state.error_message:
    st.error(f'### Error\n*{st.session_state.error_message}*')
  if st.button('Registrar', disabled=bool(st.session_state.error_message)):
    id = str(uuid4())
    tm.loc[id] = [
      work_id,
      description,
      'one_time' if category == 'Única' else 'monthly',
      pd.to_datetime(date_transaction),
      pd.to_datetime(end_transaction),
      'exprense' if mov_type == 'Gasto' else 'income',
      amount,
      stabilization_fund_percentage,
      subject
    ]
    st.rerun()

@st.dialog("Retirar de fondo de emergencia")
def cashout():  
  st.session_state.error_message = None
  # Description Validation
  description = st.text_input("Asunto:", placeholder="Descripción de la transacción")
  st.session_state.error_message = st.session_state.error_message if len(description.strip()) > 0 else 'La descripción de su transacción es obligatoria.'
  
  # Work Validation
  work_id = st.selectbox('Obra relacionada:', w['name'], index = None, placeholder='Selecciona una obra')
  
  mov_type = 'Gasto'

  # Subject validation
  subject = st.text_input('Destinatario:' if mov_type == 'Gasto' else 'Origen', placeholder="Nombre de la empresa o persona")
  st.session_state.error_message = st.session_state.error_message if len(subject.strip()) > 0 else 'El sujeto de su movimiento es obligatorio.'
  
  category = st.selectbox("Categoría:", ["Mensual", "Única"], index=1, placeholder='Selecciona una frecuencia')
  amount = st.number_input("Monto total:", step=10000)
  st.session_state.error_message = st.session_state.error_message if amount > 0 else 'El monto debe ser mayor que cero.'
  
  date_transaction = st.date_input("Fecha de transacción:")
  end_transaction = pd.NaT
  
  if category == "Mensual":
    end_transaction = st.date_input("Fecha de finalización:")
  stabilization_fund_percentage = 0
  if st.session_state.error_message:
    st.error(f'### Error\n*{st.session_state.error_message}*')
  if st.button('Registrar', disabled=bool(st.session_state.error_message)):
    id = str(uuid4())
    tm.loc[id] = [
      work_id,
      description,
      'one_time' if category == 'Única' else 'monthly',
      pd.to_datetime(date_transaction),
      pd.to_datetime(end_transaction),
      'exprense' if mov_type == 'Gasto' else 'income',
      amount,
      stabilization_fund_percentage,
      subject
    ]
    st.rerun()
