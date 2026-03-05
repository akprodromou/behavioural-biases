import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import matplotlib.font_manager as fm
import os

# -------------------------
# Font setup (Matching your project style)
# -------------------------
font_path = 'fonts/DM_Sans/DMSans-VariableFont_opsz,wght.ttf'
if os.path.exists(font_path):
    fe = fm.FontEntry(fname=font_path, name='DM Sans')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = fe.name
else:
    plt.rcParams['font.family'] = 'sans-serif'

# -------------------------
# Plot
# -------------------------
fig, ax = plt.subplots(figsize=(8, 6))

# Create the Venn diagram
# (10, 10, 4) represents sizes: (Left circle, Right circle, Intersection)
v = venn2(subsets=(10, 10, 4), 
          set_labels=('Bank Tellers', 'Active in\nFeminist Movement'),
          set_colors=('#1a73e8', '#e88f1a'), 
          alpha=0.7)

# Style the labels
for text in v.set_labels:
    text.set_fontsize(12)
    text.set_fontweight('bold')

# Highlight the intersection (The "Linda" Fallacy)
# People intuitively rank this intersection as MORE likely than the 'Bank Teller' set
v.get_label_by_id('11').set_text('Bank Teller &\nFeminist')
v.get_label_by_id('11').set_color('white')
v.get_label_by_id('11').set_fontweight('bold')

# Clear out the counts (01 and 10) to keep it conceptual
v.get_label_by_id('10').set_text('')
v.get_label_by_id('01').set_text('')

plt.title(
    "The Conjunction Fallacy (The Linda Problem)",
    loc='center',
    fontsize=15,
    fontweight=700,
    pad=20
)

# Note: The fallacy occurs because mathematically, 
# P(Bank Teller & Feminist) ≤ P(Bank Teller)
plt.annotate(
    'The Fallacy: People often rank this\nintersection as more probable than\nthe "Bank Teller" circle alone.',
    xy=v.get_label_by_id('11').get_position() - [0, 0.2],
    xytext=(0, -60),
    ha='center',
    textcoords='offset points',
    bbox=dict(boxstyle='round,pad=0.5', fc='#f8f9fa', ec='grey', alpha=0.9),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='grey')
)

plt.show()