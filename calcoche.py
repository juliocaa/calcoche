
import streamlit as st
import pandas as pd

def calculate_cost(purchase_price, fuel_price, consumption, insurance, financing, months, interest_rate, annual_km, years, maintenance):
    if financing:
        monthly_payment = (purchase_price * interest_rate / 12) / (1 - (1 + interest_rate / 12)**(-months))
        purchase_cost = monthly_payment * months
    else:
        monthly_payment = 0
        purchase_cost = purchase_price

    fuel_cost = (annual_km / 100) * fuel_price * consumption
    total_cost = purchase_cost + (fuel_cost + insurance + maintenance) * years
    monthly_cost = (monthly_payment * min(months, years * 12) + fuel_cost * years + insurance * years + maintenance * years) / (years * 12)
    
    return monthly_cost, total_cost

st.title("Coste Coche eléctrico VS Combustión")

# Datos sin valores predeterminados
electric_purchase_price = st.number_input("Coste de adquisición del coche eléctrico", value=0)
combustion_purchase_price = st.number_input("Coste de adquisición del coche de combustión", value=0)
years = st.number_input("Años para el cálculo del coste total", value=5)

# Desplegable para más opciones
with st.expander("Más opciones"):
    # Datos con valores predeterminados
    electric_insurance = st.number_input("Coste anual del seguro eléctrico", value=500)
    combustion_insurance = st.number_input("Coste anual del seguro de combustión", value=500)
    electric_consumption = st.number_input("Consumo eléctrico (kWh/100km)", value=17)
    gas_type = st.selectbox("Tipo de combustible", ("Gasolina", "Diésel"))
    combustion_consumption = st.number_input(f"Consumo de {gas_type} (l/100km)", value=7 if gas_type == "Gasolina" else 6)
    financing = st.checkbox("Financiamiento")
    months = st.number_input("Meses de financiamiento", value=84)
    interest_rate = st.number_input("Tasa de interés (%)", value=6) / 100
    annual_km = st.number_input("Kilómetros anuales", value=20000)
    electric_maintenance = st.number_input("Coste de mantenimiento eléctrico/año", value=100)
    combustion_maintenance = st.number_input("Coste de mantenimiento de combustión/año", value=300)

fuel_prices = {"Gasolina": 1.7, "Diésel": 1.5, "Electricidad": 0.15}
    
electric_monthly, electric_total = calculate_cost(
    electric_purchase_price, fuel_prices["Electricidad"], electric_consumption, electric_insurance,
    financing, months, interest_rate, annual_km, years, electric_maintenance
)
    
combustion_monthly, combustion_total = calculate_cost(
    combustion_purchase_price, fuel_prices[gas_type], combustion_consumption, combustion_insurance,
    financing, months, interest_rate, annual_km, years, combustion_maintenance
)

# Crear tabla de resultados
df = pd.DataFrame({
    "Tipo": ["Eléctrico", "Combustión"],
    "Coste mensual": [round(electric_monthly), round(combustion_monthly)],
    "Coste total": [round(electric_total), round(combustion_total)]
})

st.table(df)
