import streamlit as st
from time import sleep
from utils.store import transaction_movement as tm
from utils.auth0 import getAuth0

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

if getAuth0():

    
    col1, col2 = st.columns(2)
    col1.write("#### Transacciones")
    mov_df = tm.copy()
    mov_df['date'] = mov_df['date'].dt.strftime('%Y-%m-%d')
    mov_df = mov_df.set_index('date')

    mov_df = mov_df[['description', 'amount', 'transaction_type']]
    
    # mov_df = mov_df.style.map(lambda x: f"background-color: {'green' if x=='income' else 'red'}", subset='transaction_type')
    print(mov_df.columns)
    col1.dataframe(mov_df)

else:
    sleep(1)
    st.error('Inicia sesión para continuar.')