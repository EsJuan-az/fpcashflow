
import streamlit as st
from time import sleep
from utils.store import work as w
from utils.auth0 import getAuth0 
from ui.modals import register_work
st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)


if getAuth0():
  cols = st.columns(5)
  cols[0].write('## Obras')
  if cols[-1].button('Añadir Obra'):
    register_work()
  col1, col2, col3 = st.columns(3)
  nworks = w.shape[0]
  potential_payment = w['stipulated_payment'].sum()
  payment_deviation = w['stipulated_payment'].std()
  col1.metric(label="# de Obras", value=f"{nworks:,.0f}")
  col2.metric(label="Pago Potencial", value=f"${potential_payment:,.0f}")
  col3.metric(label="Desviación de Pagos", value=f"${payment_deviation:,.2f}")
  st.write(w)

else:
    sleep(1)
    st.error('Inicia sesión para continuar.')