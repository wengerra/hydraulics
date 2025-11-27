import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Seite konfigurieren ---
st.set_page_config(page_title="Darcy-Weisbach", layout="wide")
st.markdown(
    "<div style='font-size:18px; font-weight:bold;'>Kontinuierliche Verluste nach Darcy-Weisbach</div>",
    unsafe_allow_html=True
)

plt.rcParams.update({'font.size': 12})
g = 9.81

# ΔH-Funktion
def delta_H(lmbda, L, D, Q):
    v = 4 * Q / (np.pi * D**2)
    return lmbda * (L / D) * (v**2) / (2 * g)

# --- Sidebar Sliders ---
st.sidebar.header("Parameter")
lambda_val = st.sidebar.slider("λ (Reibungsbeiwert)", 0.01, 0.05, 0.04, 0.001, format="%.3f")
L_val      = st.sidebar.slider("L (Rohrlänge) [m]", 10, 100, 80, 5)
D_val      = st.sidebar.slider("D (Durchmesser) [m]", 0.25, 0.3, 0.28, 0.01, format="%.2f")
Q_point    = st.sidebar.slider("Q (Punkt) [m³/s]", 0.0, 0.3, 0.24, 0.01, format="%.2f")

# --- Werte für Plot ---
Q_range = np.linspace(0, 0.5, 200)
lambda_ref = 0.04
L_ref = 80
D_ref = 0.28

ref_curve = delta_H(lambda_ref, L_ref, D_ref, Q_range)
var_curve = delta_H(lambda_val, L_val, D_val, Q_range)
hr_point = delta_H(lambda_val, L_val, D_val, Q_point)

# --- Plot ---
fig, ax = plt.subplots(figsize=(10,5))  # flacherer Plot, passt besser auf Bildschirm

# Formel oben
fig.suptitle(
    r'$h_r = \lambda \cdot \frac{L}{D} \cdot \frac{v^2}{2g} '
    r'= \lambda \cdot \frac{L}{D} \cdot \frac{\left(\frac{4Q}{\pi D^{2}}\right)^{2}}{2g} '
    r'= \frac{8 \cdot \lambda \cdot L \cdot Q^2}{g \cdot \pi^2 \cdot D^5}$',
    fontsize=16,
    y=1.0
)

# Kurven
ax.plot(Q_range, ref_curve, "k--", label="Referenzkurve")
ax.plot(Q_range, var_curve, "b", label="Aktuelle Kurve")
ax.plot(Q_point, hr_point, "ro", markersize=8)

# Label Punkt
ax.text(
    Q_point,
    hr_point + 0.1*np.max(ref_curve),  # Abstand proportional Plot
    f"Q = {Q_point:.2f} m³/s\n$h_r$ = {hr_point:.1f} m",
    fontsize=12,
    color="red",
    ha="left",
    va="bottom",
    bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.2")
)

# Achsen und Limits fixieren
ax.set_xlabel("Durchfluss Q [m³/s]")
ax.set_ylabel("Verlusthöhe $h_r$ [m]")
ax.grid(True)
ax.legend()
ax.set_xlim(0, 0.5)
ax.set_ylim(0, 50)

# --- Plot anzeigen ---
st.pyplot(fig)




























