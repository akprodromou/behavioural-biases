import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_court(ax):
    # Hoop
    hoop = patches.Circle((0, 1.75), radius=0.75, linewidth=2, color='black', fill=False)
    ax.add_patch(hoop)
    
    # Backboard
    ax.plot([-3, 3], [1, 1], color='black', lw=2)
    
    # Paint (The Key)
    paint = patches.Rectangle((-8, 0), 16, 19, linewidth=2, color='black', fill=False)
    ax.add_patch(paint)
    
    # 3-point line (Straight sides and the arc)
    ax.plot([-22, -22], [0, 14], color='black', lw=2)
    ax.plot([22, 22], [0, 14], color='black', lw=2)
    three_arc = patches.Arc((0, 4.75), 47.5, 47.5, theta1=22, theta2=158, linewidth=2, color='black')
    ax.add_patch(three_arc)
    paint_arc = patches.Arc((0, 19), 16, 16, theta1=0, theta2=180, linewidth=2, color='black')
    ax.add_patch(paint_arc)
    
    # Baseline
    ax.plot([-25, 25], [0, 0], color='black', lw=2)

# Setup plot
fig, ax = plt.subplots(figsize=(8, 7.5))
draw_court(ax)

# Locations for four 3-pointers made (marked with x)
shots_x = [-21, 24, -15, 5]
shots_y = [18, 2, 28, 30]
ax.scatter(shots_x, shots_y, marker='x', color='black', s=100)

# Formatting
ax.set_xlim(-26, 26)
ax.set_ylim(-1, 48)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('white')

plt.tight_layout()
plt.show()