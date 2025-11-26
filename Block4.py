import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="h_r – Verlusthöhe Tool", layout="wide")

plt.rcParams.update({'font.size': 12})
g = 9.81

# ΔH (Darcy-Weisbach)
def delta_H(lmbda, L, D, Q):
    v = 4 * Q / (np.pi * D**2)
    return lmbda * (L / D) * (v**2) / (2 * g)

# ---------- Sidebar Controls ----------
st.sidebar.header("Parameter")
lambda_val = st.sidebar.slider("λ (Reibungsbeiwert)", 0.01, 0.05, 0.03, 0.001)
L_val      = st.sidebar.slider("L (Rohrlänge) [m]", 10, 50, 30, 5)
D_val      = st.sidebar.slider("D (Durchmesser) [m]", 0.1, 0.5, 0.3, 0.025)
Q_point    = st.sidebar.slider("Q (Punkt) [m³/s]", 0.0, 0.5, 0.25, 0.025)

# ---------- Werte für Plot ----------
Q_range = np.linspace(0, 0.5, 200)
lambda_ref = 0.03
L_ref = 30
D_ref = 0.3

ref_curve = delta_H(lambda_ref, L_ref, D_ref, Q_range)
var_curve = delta_H(lambda
