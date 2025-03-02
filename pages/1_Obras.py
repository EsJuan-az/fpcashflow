
import streamlit as st
from time import sleep
from utils.store import work as w, transaction_movement as tm
from utils.auth0 import getAuth0 
from ui.modals import register_work
import seaborn as sns
import matplotlib.pyplot as plt
st.sidebar.image("https://5pa.co/5PA/web/images/Logo_5PA2.PNG", use_container_width=True)

query_params = st.query_params
work_id = query_params.get("id", None) # Tomar el primer valor de "id"




def works_view():
  cols = st.columns(5)
  cols[0].write('## Obras')
  if cols[-1].button('Añadir Obra'):
      st.write("📌 Aquí podrías llamar a `register_work()` para agregar una obra.")

  # 📌 Estadísticas
  col1, col2, col3 = st.columns(3)
  nworks = w.shape[0]
  potential_payment = w['stipulated_payment'].sum()
  payment_deviation = w['stipulated_payment'].std()
  col1.metric(label="# de Obras", value=f"{nworks:,.0f}")
  col2.metric(label="Pago Potencial", value=f"${potential_payment:,.0f}")
  col3.metric(label="Desviación de Pagos", value=f"${payment_deviation:,.2f}")

  # 📌 Diccionario de nombres para la tabla
  rename_map = {
      'name': 'Nombre del Trabajo', 
      'stipulated_payment': 'Pago estipulado', 
      'start_date': 'Fecha de Inicio', 
      'end_date': 'Fecha de Finalización'
  }

  # Crear tabla con enlaces
  work_cp = w.copy()
  work_cp['Ver Detalles'] = work_cp.index.map(lambda wid: f"[🔍 Ver](./Obras?id={wid})")

  # 📌 Mostrar tabla con enlaces
  st.markdown("### 📋 Lista de Obras")
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
              <th>Pago Estipulado</th>
              <th>Fecha de Inicio</th>
              <th>Fecha de Finalización</th>
              <th>Ver Detalles</th>
          </tr>
      </thead>
      <tbody>
  """

  # Agregar filas con datos
  for wid, row in w.iterrows():
      table_html += f"""
    <tr>
        <td>{row['name']}</td>
        <td>${row['stipulated_payment']:,.0f}</td>
        <td>{row['start_date'].date()}</td>
        <td>{row['end_date'].date()}</td>
        <td><a href="./Obras?id={wid}" target="_self">🔍 Ver</a></td>
    </tr>
      """

  table_html += "</tbody></table>"

  # 📌 Mostrar tabla en Streamlit con HTML
  st.markdown(table_html, unsafe_allow_html=True)


def single_work_view():
  selected_work = w.loc[work_id]
  # 📌 Filtrar transacciones relacionadas con la obra
  work_transactions = tm[tm['work_id'] == work_id]

  # 🎨 Configuración de Estilos
  st.title(f"📍 {selected_work['name']}")
  
  col1, col2 = st.columns(2)
  with col1:
      st.metric(label="💰 Pago Estipulado", value=f"${selected_work['stipulated_payment']:,.2f}")
      st.metric(label="📅 Fecha de Inicio", value=selected_work['start_date'].strftime("%Y-%m-%d"))
  with col2:
      st.metric(label="🔚 Fecha de Fin", value=selected_work['end_date'].strftime("%Y-%m-%d"))
      st.metric(label="📊 Total Transacciones", value=len(work_transactions))

  # 📊 Estadísticas de Transacciones
  st.subheader("📈 Estadísticas Financieras")
  total_income = work_transactions[work_transactions["transaction_type"] == "income"]["amount"].sum()
  total_expense = work_transactions[work_transactions["transaction_type"] == "expense"]["amount"].sum()
  total_stabilization = (work_transactions["amount"] * work_transactions["stabilization_fund_percentage"] / 100).sum()
  col1, col2, col3 = st.columns(3)
  
  col1.metric(label="💵 Total Ingresos", value=f"${total_income:,.2f}")
  col2.metric(label="💸 Total Gastos", value=f"${total_expense:,.2f}")
  col3.metric(label="🏦 Fondo de Estabilización", value=f"${total_stabilization:,.2f}")

  # 📊 Gráficos
  st.subheader("📊 Visualización de Transacciones")
  
  fig, ax = plt.subplots(1, 2, figsize=(12, 5))

  # Gráfico de Distribución de Montos
  sns.histplot(work_transactions['amount'], bins=10, kde=True, ax=ax[0])
  ax[0].set_title("Distribución de Montos")
  
  # Gráfico de Tipos de Transacción
  sns.countplot(x="transaction_type", data=work_transactions, ax=ax[1])
  ax[1].set_title("Distribución de Tipos de Transacción")

  st.pyplot(fig)

  # 📜 Mostrar Detalles de las Transacciones
  st.subheader("📑 Transacciones Relacionadas")
  columnas_renombradas = {
    'date': 'Fecha',
    'description': 'Descripción',
    'transaction_type': 'Tipo de Transacción',
    'amount': 'Monto',
    'stabilization_fund_percentage': 'Porcentaje del Fondo de Estabilización'
  }
  # Renombrar las columnas del DataFrame
  work_transactions_renombrado = work_transactions.rename(columns=columnas_renombradas)
  # Seleccionar las columnas a mostrar con los nuevos nombres
  columnas_a_mostrar = list(columnas_renombradas.values())
  # Mostrar el DataFrame en Streamlit
  st.dataframe(work_transactions_renombrado[columnas_a_mostrar])


def go_back():
  st.markdown("""
    <form action="/Obras">
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
  if not work_id:
    works_view()
  elif work_id and work_id in w.index.array:
    go_back()
    single_work_view()
  else:
    go_back()
    st.warning("⚠️ No se encontró la obra. Asegúrate de ingresar un ID válido en la URL.")  
else:
  sleep(1)
  st.error('Inicia sesión para continuar.')