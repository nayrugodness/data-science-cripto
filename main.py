import streamlit as st
from datetime import datetime

from src.config import validate_config
from src.services import DashboardService
from src.utility import (
    create_comparison_bar_chart,
    create_token_volume_chart,
    format_number_with_commas
)

# Validación de configuración
validate_config()

# --- Initialize service ---
dashboard = DashboardService()

# --- Configuración de página ---
st.set_page_config(layout="wide", page_title="Dashboard COPM vs COPW")

# --- Streamlit ---
st.title("Dashboard de adopción COPM vs COPW")
st.markdown(f"*Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# Botón de refresco
if st.button("Actualizar datos"):
    st.experimental_rerun()

# --- Obtener data ---
df_copm, df_copw = dashboard.get_holders_data()

# --- Tablas lado a lado ---
st.subheader("Holders por token")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**COPM**")
    if not df_copm.empty:
        st.dataframe(dashboard.get_display_data(df_copm), use_container_width=True)
    else:
        st.warning("No hay datos para COPM")

with col2:
    st.markdown("**COPW**")
    if not df_copw.empty:
        st.dataframe(dashboard.get_display_data(df_copw), use_container_width=True)
    else:
        st.warning("No hay datos para COPW")

# --- Métricas principales ---
st.subheader("Métricas principales")
copm_metrics, copw_metrics = dashboard.get_metrics(df_copm, df_copw)

metrics_col1, metrics_col2 = st.columns(2)

with metrics_col1:
    if not df_copm.empty:
        metrics_col1.metric("COPM - Total holders", copm_metrics['total_holders'])
        metrics_col1.metric("COPM - Active holders", copm_metrics['active_holders'])
        metrics_col1.metric("COPM - Balance promedio", format_number_with_commas(copm_metrics['average_balance']))
    else:
        metrics_col1.write("No hay datos COPM")

with metrics_col2:
    if not df_copw.empty:
        metrics_col2.metric("COPW - Total holders", copw_metrics['total_holders'])
        metrics_col2.metric("COPW - Active holders", copw_metrics['active_holders'])
        metrics_col2.metric("COPW - Balance promedio", format_number_with_commas(copw_metrics['average_balance']))
    else:
        metrics_col2.write("No hay datos COPW")

# --- Comparativa de adopción ---
st.subheader("Comparativa de adopción")
compare_df = dashboard.get_comparison_data(df_copm, df_copw)
fig = create_comparison_bar_chart(compare_df)
st.plotly_chart(fig, use_container_width=True)

