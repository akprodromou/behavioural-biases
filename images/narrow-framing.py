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
# Parameters
# -------------------------
np.random.seed(10)

weeks = 52
days_per_week = 5
trading_days = weeks * days_per_week   # 260 days
dt = 1 / 252  # financial convention
start_price = 100

# Annual targets
stock_target_return = 0.05
bond_target_return = 0.03

# Annual volatility assumptions
stock_vol_annual = 0.25
bond_vol_annual = 0.05

# Daily vol
stock_vol_daily = stock_vol_annual / np.sqrt(252)
bond_vol_daily = bond_vol_annual / np.sqrt(252)

# Log return drift
stock_mu = np.log(1 + stock_target_return)
bond_mu = np.log(1 + bond_target_return)

# -------------------------
# Simulate daily paths
# -------------------------
def simulate_path(mu, sigma_daily, sigma_annual):
    shocks = np.random.normal(0, 1, trading_days)
    drift = (mu - 0.5 * sigma_annual**2) * dt
    diffusion = sigma_daily * shocks
    log_returns = drift + diffusion
    cumulative = np.cumsum(log_returns)
    prices = start_price * np.exp(cumulative)
    prices[0] = start_price
    return prices

stock_daily = simulate_path(stock_mu, stock_vol_daily, stock_vol_annual)
bond_daily = simulate_path(bond_mu, bond_vol_daily, bond_vol_annual)

# Force exact ending values
stock_daily *= (start_price * 1.05) / stock_daily[-1]
bond_daily *= (start_price * 1.03) / bond_daily[-1]

# -------------------------
# Convert to weekly properly
# -------------------------
stock_weekly = stock_daily.reshape(weeks, days_per_week)[:, -1]
bond_weekly = bond_daily.reshape(weeks, days_per_week)[:, -1]

weeks_axis = np.arange(weeks)

# -------------------------
# Plot
# -------------------------
fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(
    weeks_axis,
    stock_weekly,
    color='#e88f1a',
    linewidth=2.5,
    label="Stocks (+5%)"
)

ax.plot(
    weeks_axis,
    bond_weekly,
    color='#1a73e8',
    linewidth=2.5,
    label="Government Bonds (+3%)"
)

# Styling
ax.set_xlim(0, 51)
ax.set_ylim(80, 120)

ax.set_xlabel("Week", fontsize=11)
ax.set_ylabel("Index Value (Base = 100)", fontsize=11)

ax.set_title(
    "Stocks vs Government Bonds: performance over a year",
    loc='left',
    fontsize=15,
    fontweight=700,
    pad=15
)

ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=False)

plt.tight_layout()
plt.show()