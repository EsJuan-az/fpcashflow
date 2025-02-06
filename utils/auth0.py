from auth0_component import login_button
import streamlit as st
from utils.env import config
# Importa variables privadas de entorno

def getAuth0():
    with st.sidebar:
        user_info = login_button(config['AUTH0_CLIENT_ID'], domain = config['AUTH0_DOMAIN'])
    return user_info