import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# Load the font file
font_path = 'fonts/DM_Sans/DMSans-VariableFont_opsz,wght.ttf'
if os.path.exists(font_path):
    fe = fm.FontEntry(
        fname=font_path,
        name='DM Sans')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = fe.name
else:
    print("Font file not found, falling back to sans-serif")
    plt.rcParams['font.family'] = 'sans-serif'

# Data for the left chart 
weeks_left = np.arange(0, 7)
perf_left = [148, 140, 132, 122, 115, 105, 109]

# Data for the right chart (52 weeks)
# Weeks 0-44: dropping values
np.random.seed(42)
perf_drop = np.linspace(350, 130, 45) + np.random.normal(0, 10, 45)
# Last 7 weeks: same as perf_left
perf_right = np.concatenate([perf_drop, perf_left])
weeks_right = np.arange(0, 52)

# Create figure with two subplots side-by-side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

# --- LEFT CHART ---
ax1.plot(weeks_left, perf_left, marker='o', color='#1a73e8', linewidth=2)
# ax1.axvline(x=4, linestyle='--', color='gray', alpha=0.7)
ax1.set_ylim(0, 180)
ax1.set_xlim(left=0)
# ax1.annotate(
#     "New competitor emerges",
#     xy=(4, 145),
#     xytext=(1.5, 165),
#     arrowprops=dict(arrowstyle="->", color='black'),
#     fontsize=10
# )
ax1.set_xlabel("Week", fontsize=10)
ax1.set_ylabel("Stock Price", fontsize=10)
ax1.set_title("Stock performance the past 7 weeks", loc='left', fontsize=14, fontweight=700, pad=15)
ax1.grid(False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# --- RIGHT CHART ---
ax2.plot(weeks_right, perf_right, color='#1a73e8', linewidth=2, alpha=0.6)
# Highlight the last 7 weeks for clarity
ax2.plot(weeks_right[45:], perf_right[45:], color='#d93025', markersize=4, label='Past 7 Weeks')

ax2.set_ylim(0, 400)
ax2.set_xlim(0, 52)
ax2.set_xlabel("Week", fontsize=10)
ax2.set_ylabel("Stock Price", fontsize=10)
ax2.set_title("Stock performance the past year", loc='left', fontsize=14, fontweight=700, pad=15)
ax2.grid(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=False)

plt.tight_layout()
plt.show()