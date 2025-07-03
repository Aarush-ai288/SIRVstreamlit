
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.set_page_config(page_title="SIRV Measles Dashboard", layout="wide")

st.title("SIRV Measles Outbreak Simulator Dashboard")

st.markdown("""
This app simulates the spread of measles using a SIRV model in Gaines County, Texas.
You can adjust the parameters using the sidebar to observe how different factors impact the outbreak.
""")

def sirv_model(y, t, beta, gamma, nu):
    S, I, R, V = y
    dSdt = -beta * S * I - nu * S
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    dVdt = nu * S
    return [dSdt, dIdt, dRdt, dVdt]

# Sidebar Inputs
st.sidebar.header("Model Parameters")

N = st.sidebar.number_input("Population", value=50000, step=1000)
I0 = st.sidebar.number_input("Initial Infected", value=10)
V0_percent = st.sidebar.slider("Initial Vaccinated (%)", 0, 100, 85)
beta = st.sidebar.slider("Infection Rate (β)", 0.0, 1.0, 0.6)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.0, 1.0, 0.2)
nu = st.sidebar.slider("Vaccination Rate (ν)", 0.0, 0.1, 0.001)
days = st.sidebar.slider("Simulation Days", 30, 365, 180)

# Initial values
V0 = int((V0_percent/100) * N)
R0 = 0
S0 = N - I0 - R0 - V0
y0 = [S0/N, I0/N, R0/N, V0/N]
t = np.linspace(0, days, days)

# Solve ODE
solution = odeint(sirv_model, y0, t, args=(beta, gamma, nu))
S, I, R, V = solution.T

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, S, label='Susceptible')
ax.plot(t, I, label='Infected')
ax.plot(t, R, label='Recovered')
ax.plot(t, V, label='Vaccinated')
ax.set_xlabel('Days')
ax.set_ylabel('Fraction of Population')
ax.set_title('SIRV Model Simulation')
ax.legend()
ax.grid(True)

st.pyplot(fig)
