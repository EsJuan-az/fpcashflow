import streamlit as st
from time import sleep
from utils.store import suppliers as s, products as p
from utils.auth0 import getAuth0 
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

query_params = st.query_params
supp_id = query_params.get("id", None)  # Tomar el primer valor de "id"

def suppliers_view():
    cols = st.columns(3)
    cols[0].write('## Proveedores')
    if cols[-1].button('Añadir Proveedor'):
        st.write("📌 Aquí podrías llamar a `register_supplier()` para agregar un proveedor.")

    # 📌 Estadísticas
    col1, col2 = st.columns(2)
    nsuppliers = s.shape[0]
    total_products = p.shape[0]  # Total de productos en el sistema
    col1.metric(label="No. de Proveedores", value=f"{nsuppliers:,.0f}")
    col2.metric(label="Total de Productos", value=f"{total_products:,.0f}")

    # 📌 Calcular el número de productos por proveedor
    s['total_products'] = s.index.map(lambda sid: p[p['supplier_id'] == sid].shape[0])

    # 📌 Diccionario de nombres para la tabla
    rename_map = {
        'name': 'Nombre del Proveedor', 
        'contact': 'Contacto', 
        'nit': 'NIT', 
        'location': 'Ubicación',
        'total_products': 'Total de Productos'
    }

    # Crear tabla con enlaces
    supp_cp = s.copy()
    supp_cp['Ver Detalles'] = supp_cp.index.map(lambda sid: f"[🔍 Ver](./Proveedores?id={sid})")

    # 📌 Mostrar tabla con enlaces
    st.markdown("### 📋 Lista de Proveedores")
    table_html = """
    <style>
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 8px 12px; border-bottom: 1px solid #ddd; }
        th { background-color: #f4f4f4; color: #333 }
        a { text-decoration: none; color: #1f77b4; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
    <table>
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Contacto</th>
                <th>NIT</th>
                <th>Ubicación</th>
                <th>Total de Productos</th>
                <th>Ver Detalles</th>
            </tr>
        </thead>
        <tbody>
    """

    # Agregar filas con datos
    for sid, row in s.iterrows():
        table_html += f"""
      <tr>
          <td>{row['name']}</td>
          <td>{row['contact']}</td>
          <td>{row['nit']}</td>
          <td>{row['location']}</td>
          <td>{row['total_products']}</td>
          <td><a href="./Proveedores?id={sid}" target="_self">🔍 Ver</a></td>
      </tr>
        """

    table_html += "</tbody></table>"

    # 📌 Mostrar tabla en Streamlit con HTML
    st.markdown(table_html, unsafe_allow_html=True)

def single_supplier_view():
    selected_supplier = s.loc[supp_id]
    
    st.title(f"📍 {selected_supplier['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📞 Contacto", value=selected_supplier['contact'])
        st.metric(label="📍 Ubicación", value=selected_supplier['location'])
    with col2:
        st.metric(label="📄 NIT", value=selected_supplier['nit'])
        st.metric(label="📦 Total de Productos", value=p[p['supplier_id'] == supp_id].shape[0])

    # 📌 Mostrar productos del proveedor
    st.subheader("📦 Productos del Proveedor")
    supplier_products = p[p['supplier_id'] == supp_id]
    if not supplier_products.empty:
        st.dataframe(supplier_products[['name', 'stack_price', 'stack_amount', 'category', 'unit']])
    else:
        st.warning("Este proveedor no tiene productos registrados.")

def go_back():
    st.markdown("""
        <form action="/Proveedores">
            <input type="submit" value="🔙 Volver" style="
                background-color: #ff4b4b;
                margin: 20px 0;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            ">
        </form>
    """, unsafe_allow_html=True)

if getAuth0():
    if not supp_id:
        suppliers_view()
    elif supp_id and supp_id in s.index.array:
        go_back()
        single_supplier_view()
    else:
        go_back()
        st.warning("⚠️ No se encontró el proveedor. Asegúrate de ingresar un ID válido en la URL.")  
else:
    sleep(1)
    st.error('Inicia sesión para continuar.')