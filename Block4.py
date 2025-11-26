import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # safe backend for Streamlit

# --- Seite konfigurieren ---
st.set_page_config(page_title="h_r – Verlusthöhe Tool", layout="wide")

plt.rcParams.update({'font.size': 12})
g = 9.81

# ΔH-Funktion
def delta_H(lmbda, L, D, Q):
    v = 4 * Q / (np.pi * D**2)
    return lmbda * (L / D) * (v**2) / (2 * g)

# --- Sidebar Sliders ---
st.sidebar.header("Parameter")
lambda_val = st.sidebar.slider("λ (Reibungsbeiwert)", 0.01, 0.05, 0.03, 0.001)
L_val      = st.sidebar.slider("L (Rohrlänge) [m]", 10, 100, 50, 5)
D_val      = st.sidebar.slider("D (Durchmesser) [m]", 0.1, 0.5, 0.25, 0.05)
Q_point    = st.sidebar.slider("Q (Punkt) [m³/s]", 0.0, 0.3, 0.15, 0.05)

# --- Werte für Plot ---
Q_range = np.linspace(0, 0.5, 200)
lambda_ref = 0.03
L_ref = 50
D_ref = 0.25

ref_curve = delta_H(lambda_ref, L_ref, D_ref, Q_range)
var_curve = delta_H(lambda_val, L_val, D_val, Q_range)
hr_point = float(delta_H(lambda_val, L_val, D_val, Q_point))  # ensure scalar

# --- Plot ---
fig, ax = plt.subplots(figsize=(10,5))

# Formel oben
fig.suptitle(
    r'$h_r = \lambda \cdot \frac{L}{D} \cdot \frac{v^2}{2g} '
    r'= \lambda \cdot \frac{L}{D} \cdot \frac{\left(\frac{4Q}{\pi D^{2}}\right)^{2}}{2g} '
    r'= \frac{8 \cdot \lambda \cdot L \cdot Q^2}{g \cdot \pi^2 \cdot D^5}$',
    fontsize=16,
    y=0.95
)

# Kurven
ax.plot(Q_range, ref_curve, "k--", label="Referenzkurve")
ax.plot(Q_range, var_curve, "b", label="Aktuelle Kurve")
ax.plot(Q_point, hr_point, "ro", markersize=8)

# Label Punkt
ax.text(
    Q_point,
    hr_point + 0.03*np.max(ref_curve),
    f"Q = {Q_point:.2f} m³/s\n$h_r$ = {hr_point:.1f} m",
    fontsize=12,
    color="red",
    ha="left",
    va="bottom",
    bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.2")
)

ax.set_xlabel("Durchfluss Q [m³/s]")
ax.set_ylabel("Verlusthöhe $h_r$ [m]")
ax.grid(True)
ax.legend()
ax.set_xlim(0, 0.4)
ax.set_ylim(0, 20)

# --- Plot anzeigen ---
st.pyplot(fig)
plt.close(fig)
