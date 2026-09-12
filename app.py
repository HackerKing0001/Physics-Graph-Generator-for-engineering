import io
import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Physics Lab Graph Generator",
    page_icon="🔬",
    layout="wide"
)

# Google Search Console ownership verification.
# Replace YOUR_CODE_HERE below with the "content" value Google gives you
# under Search Console -> Add website -> Other verification methods -> HTML tag.
st.markdown(
    '<meta name="google-site-verification" content="e4ceOcApPdH1Bqi8CXRf_FzyNcEJIaYRglnhaP0SJN8" />',
    unsafe_allow_html=True
)
st.title("🔬 Physics Lab Graph Generator")
st.caption("Enter your experimental readings and generate a clean lab graph with automatic best-fit analysis.")

PRESETS = {
    "Custom Experiment": {
        "x_label": "X",
        "x_unit": "",
        "y_label": "Y",
        "y_unit": "",
        "title": "Physics Lab Graph",
    },
    "Ohm's Law (V vs I)": {
        "x_label": "Current (I)",
        "x_unit": "A",
        "y_label": "Voltage (V)",
        "y_unit": "V",
        "title": "Ohm's Law: Voltage vs Current",
    },
    "Convex Lens (u vs v)": {
        "x_label": "Object distance (u)",
        "x_unit": "cm",
        "y_label": "Image distance (v)",
        "y_unit": "cm",
        "title": "Convex Lens: u vs v",
    },
    "Convex Lens (1/u vs 1/v)": {
        "x_label": "1/u",
        "x_unit": "cm⁻¹",
        "y_label": "1/v",
        "y_unit": "cm⁻¹",
        "title": "Convex Lens: 1/u vs 1/v",
    },
    "Prism (i vs δ)": {
        "x_label": "Angle of incidence (i)",
        "x_unit": "°",
        "y_label": "Angle of deviation (δ)",
        "y_unit": "°",
        "title": "Prism: Angle of Deviation vs Angle of Incidence",
    },
    "Meter Bridge (R vs l)": {
        "x_label": "Balance length (l)",
        "x_unit": "cm",
        "y_label": "Resistance (R)",
        "y_unit": "Ω",
        "title": "Meter Bridge: Resistance vs Balance Length",
    },
    "Sonometer (L vs 1/f)": {
        "x_label": "1/f",
        "x_unit": "s",
        "y_label": "Length (L)",
        "y_unit": "cm",
        "title": "Sonometer: Length vs 1/f",
    },
    "Galvanometer (V vs I)": {
        "x_label": "Current (I)",
        "x_unit": "A",
        "y_label": "Potential difference (V)",
        "y_unit": "V",
        "title": "Galvanometer: V vs I",
    },
    "Forward V-I Characteristics (Diode)": {
        "x_label": "Forward Voltage (V)",
        "x_unit": "V",
        "y_label": "Forward Current (I)",
        "y_unit": "mA",
        "title": "Forward V-I Characteristics of a Diode",
    },
    "Reverse V-I Characteristics (Diode)": {
        "x_label": "Reverse Voltage (V)",
        "x_unit": "V",
        "y_label": "Reverse Current (I)",
        "y_unit": "μA",
        "title": "Reverse V-I Characteristics of a Diode",
    },
    "log(n) vs 1/T": {
        "x_label": "1/T",
        "x_unit": "K⁻¹",
        "y_label": "log(n)",
        "y_unit": "",
        "title": "log(n) vs 1/T",
    },
    "Diffraction Grating (sin θ vs n)": {
        "x_label": "Order (n)",
        "x_unit": "",
        "y_label": "sin θ",
        "y_unit": "",
        "title": "Diffraction Grating: sin θ vs n",
    },
    "Thermionic Emission (log I₀ vs 1/T)": {
        "x_label": "1/T",
        "x_unit": "K⁻¹",
        "y_label": "log I₀",
        "y_unit": "",
        "title": "Thermionic Emission: log I₀ vs 1/T",
    },
    "Magnetic Field (r vs x)": {
        "x_label": "Distance (x)",
        "x_unit": "cm",
        "y_label": "Radius (r)",
        "y_unit": "cm",
        "title": "r vs x",
    },
    "Newton's Rings (d vs x)": {
        "x_label": "Distance (x)",
        "x_unit": "cm",
        "y_label": "Diameter (d)",
        "y_unit": "cm",
        "title": "d vs x",
    },
    "Photoelectric Effect (K vs f)": {
        "x_label": "Frequency (f)",
        "x_unit": "Hz",
        "y_label": "Kinetic Energy (K)",
        "y_unit": "eV",
        "title": "Photoelectric Effect: K vs f",
    },
    "Stewart & Gee (y vs B²)": {
        "x_label": "B²",
        "x_unit": "T²",
        "y_label": "y",
        "y_unit": "m",
        "title": "y vs B²",
    },
}

# ---------- Helpers ----------
def parse_numbers(text):
    """Accept comma, space, semicolon, or newline separated values."""
    if not text.strip():
        return np.array([], dtype=float)
    cleaned = text.replace(",", " ").replace(";", " ").replace("\n", " ")
    values = []
    for token in cleaned.split():
        values.append(float(token))
    return np.array(values, dtype=float)

def unit_text(label, unit):
    return f"{label} ({unit})" if unit else label

def calculate_fit(x, y):
    if len(x) < 2:
        return None
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    ss_res = float(np.sum((y - y_fit) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    return slope, intercept, r2

def make_figure(x, y, title, xlabel, ylabel, fit_enabled, grid_enabled, point_labels):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        x, y,
        s=65,
        marker="o",
        label="Experimental readings",
        zorder=3
    )

    if fit_enabled and len(x) >= 2:
        fit = calculate_fit(x, y)
        if fit:
            slope, intercept, r2 = fit
            x_line = np.linspace(np.min(x), np.max(x), 200)
            y_line = slope * x_line + intercept
            ax.plot(
                x_line, y_line,
                linewidth=2,
                label=f"Best fit: y = {slope:.4g}x + {intercept:.4g}"
            )

    if point_labels:
        for i, (xx, yy) in enumerate(zip(x, y), start=1):
            ax.annotate(
                str(i),
                (xx, yy),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9
            )

    ax.set_title(title, fontsize=16, pad=12)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(grid_enabled, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Graph Settings")

    preset = st.selectbox("Experiment", list(PRESETS.keys()))
    p = PRESETS[preset]

    st.subheader("Axis labels")
    if preset == "Custom Experiment":
        x_label = st.text_input("X-axis quantity", p["x_label"])
        x_unit = st.text_input("X-axis unit", p["x_unit"])
        y_label = st.text_input("Y-axis quantity", p["y_label"])
        y_unit = st.text_input("Y-axis unit", p["y_unit"])
        title = st.text_input("Graph title", p["title"])
    else:
        x_label = p["x_label"]
        x_unit = p["x_unit"]
        y_label = p["y_label"]
        y_unit = p["y_unit"]
        title = st.text_input("Graph title", p["title"])

    graph_type = st.selectbox(
        "Graph style",
        ["Scatter + best-fit line", "Scatter only", "Connected points"]
    )
    grid_enabled = st.checkbox("Show grid", True)
    point_labels = st.checkbox("Number data points", False)

    st.divider()
    st.info(
        "Tip: For a straight-line experiment, use "
        "'Scatter + best-fit line'."
    )

# ---------- Main data input ----------
left, right = st.columns([1, 1])

with left:
    st.subheader("📥 Experimental Data")
    st.write("Enter X and Y readings. Use commas, spaces, semicolons, or new lines.")

    default_x = "1, 2, 3, 4, 5"
    default_y = "2, 4, 6, 8, 10"

    x_text = st.text_area(
        f"{x_label}" + (f" [{x_unit}]" if x_unit else ""),
        default_x,
        height=150
    )
    y_text = st.text_area(
        f"{y_label}" + (f" [{y_unit}]" if y_unit else ""),
        default_y,
        height=150
    )

with right:
    st.subheader("🧮 Analysis")
    try:
        x = parse_numbers(x_text)
        y = parse_numbers(y_text)

        if len(x) != len(y):
            st.error(f"X has {len(x)} readings but Y has {len(y)} readings.")
            valid = False
        elif len(x) < 2:
            st.warning("Enter at least 2 pairs of readings.")
            valid = False
        elif not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
            st.error("All readings must be finite numbers.")
            valid = False
        else:
            valid = True
            st.success(f"✓ {len(x)} reading pairs loaded.")

            fit = calculate_fit(x, y)

            if fit:
                slope, intercept, r2 = fit
                c1, c2, c3 = st.columns(3)
                c1.metric("Slope", f"{slope:.6g}")
                c2.metric("Intercept", f"{intercept:.6g}")
                c3.metric("R²", f"{r2:.6f}")

                st.latex(
                    rf"y = {slope:.6g}x "
                    rf"{'+' if intercept >= 0 else '-'} "
                    rf"{abs(intercept):.6g}"
                )

    except ValueError as e:
        st.error(f"Could not read the data: {e}")
        valid = False

# ---------- Graph ----------
st.divider()
st.subheader("📊 Generated Graph")

if valid:
    xlabel = unit_text(x_label, x_unit)
    ylabel = unit_text(y_label, y_unit)

    if graph_type == "Scatter + best-fit line":
        fig = make_figure(
            x, y, title, xlabel, ylabel,
            fit_enabled=True,
            grid_enabled=grid_enabled,
            point_labels=point_labels
        )
    elif graph_type == "Scatter only":
        fig = make_figure(
            x, y, title, xlabel, ylabel,
            fit_enabled=False,
            grid_enabled=grid_enabled,
            point_labels=point_labels
        )
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            x, y,
            marker="o",
            linewidth=2,
            markersize=6,
            label="Experimental readings"
        )
        if point_labels:
            for i, (xx, yy) in enumerate(zip(x, y), start=1):
                ax.annotate(str(i), (xx, yy), xytext=(6, 6),
                            textcoords="offset points")
        ax.set_title(title, fontsize=16, pad=12)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(grid_enabled, alpha=0.3)
        ax.legend()
        fig.tight_layout()

    st.pyplot(fig, clear_figure=False)

    # Data table
    with st.expander("📋 View reading table"):
        import pandas as pd
        table = pd.DataFrame({
            xlabel: x,
            ylabel: y
        })
        st.dataframe(table, use_container_width=True)

    # Downloads
    png_buffer = io.BytesIO()
    fig.savefig(png_buffer, format="png", dpi=300, bbox_inches="tight")
    png_buffer.seek(0)

    pdf_buffer = io.BytesIO()
    fig.savefig(pdf_buffer, format="pdf", bbox_inches="tight")
    pdf_buffer.seek(0)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇️ Download PNG",
            data=png_buffer,
            file_name="physics_lab_graph.png",
            mime="image/png",
            use_container_width=True
        )
    with d2:
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_buffer,
            file_name="physics_lab_graph.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    plt.close(fig)
else:
    st.info("Enter valid X and Y readings to generate the graph.")

st.divider()
st.caption("Physics Lab Graph Generator • Built with Python, Streamlit, NumPy and Matplotlib")