import streamlit as st
import pandas as pd
import numpy_financial as npf

def calculate_monthly_cost(acquisition_cost, km_per_year, fuel_cost, consumption, insurance, loan_months, loan_interest, maintenance):
    if loan_months > 0:
        monthly_payment = npf.pmt(rate=loan_interest/12, nper=loan_months, pv=-acquisition_cost)
    else:
        monthly_payment = acquisition_cost / 12  # one-time payment divided over one year
    
    fuel_cost_per_month = (km_per_year / 100) * consumption * fuel_cost / 12
    insurance_per_month = insurance / 12
    maintenance_per_month = maintenance / 12
    
    return monthly_payment + fuel_cost_per_month + insurance_per_month + maintenance_per_month

# Streamlit UI
st.title("Calculadora de coste de coches")

# Datos de entrada comunes
acquisition_cost_electric = st.number_input("Coste de adquisición del coche eléctrico:", min_value=0, value=30000)
acquisition_cost_combustion = st.number_input("Coste de adquisición del coche de combustión:", min_value=0, value=20000)
km_per_year = st.number_input("Kilómetros por año:", min_value=0, value=20000)
years = st.number_input("Años para cálculo acumulado:", min_value=1, value=5)

# Desplegable de más opciones
with st.expander("Más opciones", expanded=False):
    insurance_electric = st.number_input("Coste anual del seguro (eléctrico):", value=500)
    insurance_combustion = st.number_input("Coste anual del seguro (combustión):", value=500)
    loan_months = st.number_input("Meses de financiación:", value=84)
    loan_interest = st.number_input("Interés (%):", value=6.0)
    fuel_type = st.selectbox("Tipo de combustible:", options=["Gasolina", "Diésel"])
    
    # Valores predeterminados según el tipo de combustible
    fuel_cost = 1.7 if fuel_type == "Gasolina" else 1.5
    consumption_combustion = 7 if fuel_type == "Gasolina" else 6
    fuel_cost = st.number_input(f"Precio del {fuel_type} (€/l):", value=fuel_cost)
    consumption_combustion = st.number_input(f"Consumo cada 100km ({fuel_type}):", value=consumption_combustion)
    
    electricity_cost = st.number_input("Precio de electricidad (€/kWh):", value=0.15)
    consumption_electric = st.number_input("Consumo cada 100km (eléctrico):", value=17)
    maintenance_combustion = st.number_input("Coste de mantenimiento anual (combustión):", value=300)
    maintenance_electric = st.number_input("Coste de mantenimiento anual (eléctrico):", value=100)

# Cálculo
monthly_cost_electric = calculate_monthly_cost(acquisition_cost_electric, km_per_year, electricity_cost, consumption_electric, insurance_electric, loan_months, loan_interest / 100, maintenance_electric)
monthly_cost_combustion = calculate_monthly_cost(acquisition_cost_combustion, km_per_year, fuel_cost, consumption_combustion, insurance_combustion, loan_months, loan_interest / 100, maintenance_combustion)

# Mostrar resultados
data = {
    "Tipo de coche": ["Eléctrico", "Combustión"],
    "Coste mensual (€)": [monthly_cost_electric, monthly_cost_combustion],
    "Coste total acumulado (€)": [monthly_cost_electric * 12 * years, monthly_cost_combustion * 12 * years]
}

df = pd.DataFrame(data)
st.table(df)

