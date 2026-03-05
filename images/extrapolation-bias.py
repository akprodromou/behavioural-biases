import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# -------------------------
# Font setup
# -------------------------
font_path = 'fonts/DM_Sans/DMSans-VariableFont_opsz,wght.ttf'
if os.path.exists(font_path):
    fe = fm.FontEntry(fname=font_path, name='DM Sans')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = fe.name
else:
    print("Font file not found, falling back to sans-serif")
    plt.rcParams['font.family'] = 'sans-serif'

# -------------------------
# Generate main rising data (26 weeks)
# -------------------------
np.random.seed(42)

weeks_actual = np.arange(0, 26)

trend = np.linspace(100, 180, 26)
noise = np.random.normal(0, 4, 26)
price_actual = trend + noise

# -------------------------
# Generate 3 hypothetical future scenarios
# -------------------------
weeks_future = np.arange(25, 52)

future_scenarios = []

for i in range(3):
    drift_scalar = np.random.uniform(-1.5, 2.5)
    
    drift = np.insert(np.full(len(weeks_future) - 1, drift_scalar), 0, 0)
    noise = np.insert(np.random.normal(0, 6, len(weeks_future) - 1), 0, 0)

    future_path = price_actual[-1] + np.cumsum(drift + noise)

    future_scenarios.append(future_path)

# -------------------------
# Plot
# -------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# Actual line
ax.plot(
    weeks_actual,
    price_actual,
    color='#1a73e8',
    linewidth=2.5,
    marker='o',
    label="Actual price"
)

# Future dashed grey scenarios
for scenario in future_scenarios:

    ax.plot(
        weeks_future,
        scenario,
        linestyle='--',
        color='grey',
        alpha=0.6,
        linewidth=2
    )

# Vertical separator
ax.axvline(
    x=25,
    linestyle=':',
    color='grey',
    alpha=0.7
)

# -------------------------
# Styling
# -------------------------
ax.set_xlim(0, 52)
ax.set_ylim(80, 260)

ax.set_xlabel("Week", fontsize=11)
ax.set_ylabel("Stock Price", fontsize=11)

ax.set_title(
    "Stock Performance and Possible Future Paths",
    loc='left',
    fontsize=15,
    fontweight=700,
    pad=15
)

ax.grid(False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()