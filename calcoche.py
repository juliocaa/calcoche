import streamlit as st
import pandas as pd

def calculate_cost(price_fuel, consumption, distance, acquisition_cost, insurance_cost, maintenance_cost, financing_months=84, interest_rate=0.06):
    if financing_months > 0:
        monthly_payment = acquisition_cost * (interest_rate/12) / (1 - (1 + interest_rate/12)**(-financing_months))
    else:
        monthly_payment = acquisition_cost / 12
    
    fuel_cost = (distance / 100) * consumption * price_fuel
    total_monthly_cost = monthly_payment + fuel_cost + (insurance_cost/12) + (maintenance_cost/12)
    
    if financing_months > 0:
        post_financing_cost = fuel_cost + (insurance_cost/12) + (maintenance_cost/12)
    else:
        post_financing_cost = total_monthly_cost
    
    return total_monthly_cost, post_financing_cost

# Streamlit UI
st.title("Calculadora de coste de coche: Combustión vs Eléctrico")

# Datos de entrada sin valores por defecto
acquisition_cost_combustion = st.number_input("Coste de adquisición del coche de combustión", value=0)
acquisition_cost_electric = st.number_input("Coste de adquisición del coche eléctrico", value=0)
years = st.number_input("Años a tener en cuenta", value=5)

# Desplegable para más opciones
with st.beta_expander("Más opciones"):
    fuel_type = st.selectbox("Tipo de combustible", ["Gasolina", "Gasoil"])
    insurance_cost_combustion = st.number_input("Coste anual del seguro para el coche de combustión", value=500)
    insurance_cost_electric = st.number_input("Coste anual del seguro para el coche eléctrico", value=500)
    distance = st.number_input("Kilómetros anuales", value=20000)
    financing_months = st.number_input("Meses de financiación", value=84)
    interest_rate = st.number_input("Tasa de interés", value=6.0) / 100

# Constantes
default_values = {
    "Gasolina": {"price": 1.7, "consumption": 7, "maintenance": 300},
    "Gasoil": {"price": 1.5, "consumption": 6, "maintenance": 300},
    "Eléctrico": {"price": 0.15, "consumption": 17, "maintenance": 100},
}

# Cálculos
total_combustion, post_combustion = calculate_cost(
    default_values[fuel_type]["price"], default_values[fuel_type]["consumption"], distance, 
    acquisition_cost_combustion, insurance_cost_combustion, default_values[fuel_type]["maintenance"],
    financing_months, interest_rate
)

total_electric, post_electric = calculate_cost(
    default_values["Eléctrico"]["price"], default_values["Eléctrico"]["consumption"], distance, 
    acquisition_cost_electric, insurance_cost_electric, default_values["Eléctrico"]["maintenance"],
    financing_months, interest_rate
)

# Crear la tabla
df = pd.DataFrame({
    "Coche": ["Combustión", "Eléctrico"],
    "Coste Mensual": [total_combustion, total_electric],
    "Coste Post-Financiamiento": [post_combustion, post_electric]
})
st.table(df)
