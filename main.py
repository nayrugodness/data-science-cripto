import os
from dotenv import load_dotenv
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

load_dotenv()

# --- Variables de entorno ---
API_KEY = os.getenv("DUNE_API_KEY")
COPM_CHAIN_ID = int(os.getenv("CHAIN_ID_POLYGON"))
COPM_TOKEN_ADDRESS = os.getenv("COPM_TOKEN_ADDRESS")
COPW_CHAIN_ID = int(os.getenv("CHAIN_ID_ETH"))
COPW_TOKEN_ADDRESS = os.getenv("COPW_TOKEN_ADDRESS")

# Validación
for var_name, var_value in [("DUNE_API_KEY", API_KEY), 
                            ("COPM_TOKEN_ADDRESS", COPM_TOKEN_ADDRESS),
                            ("COPW_TOKEN_ADDRESS", COPW_TOKEN_ADDRESS)]:
    if var_value is None:
        raise ValueError(f"La variable de entorno {var_name} no está definida")

HEADERS = {"X-Sim-Api-Key": API_KEY}

# --- Función para obtener holders ---
def get_holders(chain_id, token_address):
    url = f"https://api.sim.dune.com/v1/evm/token-holders/{chain_id}/{token_address}"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    holders = data.get("holders", [])
    df = pd.DataFrame(holders)
    if not df.empty:
        df['balance'] = df['balance'].astype(float)
        df = df.sort_values(by='balance', ascending=False).reset_index(drop=True)
    return df

# --- Streamlit ---
st.title("Dashboard de adopción COPM vs COPW")
st.markdown(f"*Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# Botón de refresco
if st.button("Actualizar datos"):
    st.experimental_rerun()

# --- Obtener data ---
df_copm = get_holders(COPM_CHAIN_ID, COPM_TOKEN_ADDRESS)
df_copw = get_holders(COPW_CHAIN_ID, COPW_TOKEN_ADDRESS)

# --- Tablas lado a lado ---
st.subheader("Holders por token")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**COPM**")
    if not df_copm.empty:
        st.dataframe(df_copm[['wallet_address','balance','has_initiated_transfer','first_acquired']], use_container_width=True)
    else:
        st.warning("No hay datos para COPM")
with col2:
    st.markdown("**COPW**")
    if not df_copw.empty:
        st.dataframe(df_copw[['wallet_address','balance','has_initiated_transfer','first_acquired']], use_container_width=True)
    else:
        st.warning("No hay datos para COPW")

# --- Normalizar balances para gráficos ---
DECIMALS_COPM = 18
DECIMALS_COPW = 18
if not df_copm.empty:
    df_copm['balance_token'] = df_copm['balance'] / (10**DECIMALS_COPM)
if not df_copw.empty:
    df_copw['balance_token'] = df_copw['balance'] / (10**DECIMALS_COPW)

# --- Métricas principales lado a lado ---
st.subheader("Métricas principales")
metrics_col1, metrics_col2 = st.columns(2)

if not df_copm.empty:
    metrics_col1.metric("COPM - Total holders", len(df_copm))
    metrics_col1.metric("COPM - Active holders", df_copm['has_initiated_transfer'].sum())
    metrics_col1.metric("COPM - Balance promedio", f"{df_copm['balance_token'].mean():,.2f}")
else:
    metrics_col1.write("No hay datos COPM")

if not df_copw.empty:
    metrics_col2.metric("COPW - Total holders", len(df_copw))
    metrics_col2.metric("COPW - Active holders", df_copw['has_initiated_transfer'].sum())
    metrics_col2.metric("COPW - Balance promedio", f"{df_copw['balance_token'].mean():,.2f}")
else:
    metrics_col2.write("No hay datos COPW")

# --- Comparativa de adopción ---
st.subheader("Comparativa de adopción")
compare_df = pd.DataFrame({
    "Token": ["COPM","COPW"],
    "Total Holders":[len(df_copm),len(df_copw)],
    "Active Holders":[df_copm['has_initiated_transfer'].sum() if not df_copm.empty else 0,
                      df_copw['has_initiated_transfer'].sum() if not df_copw.empty else 0]
})
fig = px.bar(compare_df, x="Token", y=["Total Holders","Active Holders"], barmode='group', text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# --- Distribución de balances comparativa ---
st.subheader("Distribución de balances por token (normalizados)")
if not df_copm.empty or not df_copw.empty:
    col1, col2 = st.columns(2)
    if not df_copm.empty:
        fig_copm = px.histogram(df_copm, x='balance_token', nbins=20,
                                title="COPM - Distribución de balances",
                                labels={'balance_token':'Balance (tokens)'},
                                color_discrete_sequence=['#636EFA'])
        fig_copm.update_layout(yaxis_title="Número de holders")
        col1.plotly_chart(fig_copm, use_container_width=True)
    else:
        col1.write("No hay datos COPM")
    
    if not df_copw.empty:
        fig_copw = px.histogram(df_copw, x='balance_token', nbins=20,
                                title="COPW - Distribución de balances",
                                labels={'balance_token':'Balance (tokens)'},
                                color_discrete_sequence=['#EF553B'])
        fig_copw.update_layout(yaxis_title="Número de holders")
        col2.plotly_chart(fig_copw, use_container_width=True)
    else:
        col2.write("No hay datos COPW")
else:
    st.warning("No hay datos suficientes para mostrar balances")
