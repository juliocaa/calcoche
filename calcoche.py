import streamlit as st

st.title('Comparador de coste de coches: Combustión vs Eléctrico')

# Datos comunes
coste_adquisicion_combustion = st.number_input("Coste de adquisición del coche de combustión (€)", value=0)
coste_adquisicion_electrico = st.number_input("Coste de adquisición del coche eléctrico (€)", value=0)
coste_anual_seguro = st.number_input("Coste anual del seguro (€)", value=0)
compra_financiada = st.checkbox("Compra mediante financiación")
if compra_financiada:
    meses_financiacion = st.number_input("Meses de financiación", value=84)
    intereses = st.number_input("Intereses (%)", value=6)
km_anuales = st.number_input("Kilómetros esperados al año", value=20000)
years = st.number_input("Años a considerar para el cálculo", value=5)

# Desplegable para más opciones
with st.expander("Más opciones"):
    # Combustión
    tipo_combustible = st.selectbox("Tipo de combustible", options=["Gasolina", "Diésel"])
    if tipo_combustible == "Gasolina":
        precio_gasolina = st.number_input("Precio gasolina (€/l)", value=1.7)
        consumo_gasolina = st.number_input("Consumo gasolina (l/100km)", value=7)
    else:
        precio_gasoil = st.number_input("Precio gasoil (€/l)", value=1.5)
        consumo_gasoil = st.number_input("Consumo gasoil (l/100km)", value=6)
    coste_mantenimiento_combustion = st.number_input("Coste mantenimiento anual combustión (€)", value=300)

    # Eléctrico
    precio_kwh = st.number_input("Precio electricidad (€/kWh)", value=0.15)
    consumo_electricidad = st.number_input("Consumo electricidad (kWh/100km)", value=17)
    coste_mantenimiento_electrico = st.number_input("Coste mantenimiento anual eléctrico (€)", value=100)

# Cálculos
if compra_financiada:
    cuota_financiacion_combustion = coste_adquisicion_combustion * (intereses / 100 / 12) / (1 - (1 + intereses / 100 / 12) ** -meses_financiacion)
    cuota_financiacion_electrico = coste_adquisicion_electrico * (intereses / 100 / 12) / (1 - (1 + intereses / 100 / 12) ** -meses_financiacion)
else:
    cuota_financiacion_combustion = 0
    cuota_financiacion_electrico = 0

if tipo_combustible == "Gasolina":
    coste_mensual_combustion = (precio_gasolina * consumo_gasolina * km_anuales / 100 + coste_anual_seguro + coste_mantenimiento_combustion) / 12 + cuota_financiacion_combustion
else:
    coste_mensual_combustion = (precio_gasoil * consumo_gasoil * km_anuales / 100 + coste_anual_seguro + coste_mantenimiento_combustion) / 12 + cuota_financiacion_combustion

coste_mensual_electrico = (precio_kwh * consumo_electricidad * km_anuales / 100 + coste_anual_seguro + coste_mantenimiento_electrico) / 12 + cuota_financiacion_electrico

# Mostrar resultados
st.subheader("Resultados")
st.write(f"Coste mensual del coche de combustión: €{coste_mensual_combustion:.2f}")
st.write(f"Coste mensual del coche eléctrico: €{coste_mensual_electrico:.2f}")
st.write(f"Coste acumulado del coche de combustión en {years} años: €{coste_mensual_combustion * 12 * years:.2f}")
st.write(f"Coste acumulado del coche eléctrico en {years} años: €{coste_mensual_electrico * 12 * years:.2f}")
