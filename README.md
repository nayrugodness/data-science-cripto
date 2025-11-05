# NayruGodness - Monitoreo de adopción de tokens COPM y COPW

## Descripción

Este proyecto es una aplicación web desarrollada con **Streamlit**, desplegada directamente desde **GitHub Actions**. La app permite monitorear la adopción de dos tokens, **COPM** y **COPW**, mostrando métricas de uso y comportamiento de las wallets que los poseen.

Los datos se obtienen de **Dune Analytics**, utilizando la API para extraer información sobre transacciones y balances de los tokens.

---

## Variables de entorno

Antes de ejecutar la aplicación, debes configurar las siguientes variables de entorno en tu sistema o en Streamlit Cloud:

```bash
DUNE_API_KEY=""            # Tu API Key de Dune Analytics
CHAIN_ID_ETH=""            # ID de la cadena Ethereum
CHAIN_ID_POLYGON=""        # ID de la cadena Polygon
COPM_TOKEN_ADDRESS=""      # Dirección del token COPM
COPW_TOKEN_ADDRESS=""      # Dirección del token COPW
```

> Estas variables permiten que la app se conecte a la blockchain correcta y a Dune Analytics para obtener los datos de cada token.

---

## Tecnologías utilizadas

- **Python 3.11**  
- **Streamlit 1.29.0** para la interfaz web  
- **Pandas 2.1.1** para manejo de datos  
- **Plotly 5.15.0** para visualización interactiva  
- **Requests 2.31.0** para llamadas HTTP a la API de Dune  
- **Python-dotenv 1.1.1** para cargar variables de entorno  
- **st-autorefresh 0.1.0** para actualizar automáticamente la data en la app

---

## Flujo de datos

1. La app consulta la API de **Dune Analytics** utilizando la clave `DUNE_API_KEY`.  
2. Se obtienen métricas sobre **quién posee COPM y COPW** y cómo se comportan las wallets.  
3. Los datos se procesan con **Pandas** y se generan visualizaciones interactivas con **Plotly**.  
4. La app muestra comparativas en tiempo real para determinar cuál token tiene **mayor adopción**.

---

## Despliegue

La aplicación se despliega automáticamente en **Streamlit Cloud** mediante **GitHub Actions**:

1. Cada push al repositorio activa el workflow de GitHub Actions.  
2. Se instala el entorno virtual con las dependencias definidas en `requirements.txt`.  
3. Se ejecuta la app en Streamlit Cloud, mostrando dashboards actualizados sobre la adopción de los tokens.

---

## Ejecución local

Para ejecutar la app en tu máquina:

1. Clona el repositorio:

```bash
git clone https://github.com/nayrugodness/data-science-cripto.git
cd data-science-cripto
```

2. Crea un entorno virtual e instala dependencias:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. Configura tus variables de entorno en un archivo `.env`:

```bash
DUNE_API_KEY="TU_API_KEY"
CHAIN_ID_ETH="1"
CHAIN_ID_POLYGON="137"
COPM_TOKEN_ADDRESS="0x..."
COPW_TOKEN_ADDRESS="0x..."
```

4. Ejecuta la app:

```bash
streamlit run main/main.py
```

---

## Objetivo

El objetivo principal de esta app es **monitorear en tiempo real cuál token (COPM o COPW) tiene más adopción** y entender **cómo las wallets interactúan con ellos**. Esto permite tomar decisiones estratégicas sobre liquidez, marketing y uso de los tokens.

---

## Notas

- Se recomienda **Python 3.11**, ya que versiones más recientes como 3.13 pueden generar conflictos con dependencias de Streamlit.  
- Asegúrate de tener acceso a **Dune Analytics** y configurar correctamente tu `DUNE_API_KEY`.  
- La app refresca automáticamente los datos gracias a `st-autorefresh`.