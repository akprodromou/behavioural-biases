import os
import re

# Your matchup list
matchups = {
    "1.1.1": "Attention Bias",
    "1.1.2": "Hindsight Bias",
    "1.2.1": "Law of Small Numbers",
    "1.2.2": "Gambler’s Fallacy",
    "1.2.3": "Hot Hand Fallacy",
    "1.2.4": "Extrapolation Bias",
    "1.2.5": "Base Rate Neglect",
    "1.2.6": "Illusion of Validity",
    "1.2.7": "Causality and attribution",
    "1.3": "Affect Heuristic",
    "1.4.1": "Self-attribution Bias",
    "1.4.2": "Confirmation Bias",
    "1.4.3": "Illusion of Control",
    "1.5": "(Excessive) Optimism",
    "1.6.2": "Recognition Heuristic",
    "1.6.3": "Fluency Heuristic",
    "1.6": "Familiarity",
    "2.1.2": "Context dependence",
    "2.1.3": "Repeated gambles",
    "2.2.1": "Hedonic editing",
    "2.2.2": "Choice bracketing",
    "2.3.1.1": "Hyperbolic Discounting and Present Bias",
    "2.3.1.2": "Hyperbolic Discounting and Present Bias",
    "2.3.2": "Self-Control and Commitment",
    "2.3.3.1": "Preference Reversals",
    "2.3.3.2": "Preference Reversals",
    "2.3.3": "Preference Reversals",
    "2.4.1": "Reference Dependence",
    "2.4.2": "Loss Aversion",
    "3.1.1": "Cultural Differences",
    "3.2.1": "Obedience to authority",
    "3.4": "Fairness and Justice",
    "3.5": "Greed and fear",
    "3.6.1": "Availability Cascades",
}

# convert to slug
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


folder = "."

for filename in os.listdir(folder):

    name, ext = os.path.splitext(filename)

    if name in matchups:

        new_name = slugify(matchups[name]) + ext

        print(f"{filename} -> {new_name}")

        os.rename(
            os.path.join(folder, filename),
            os.path.join(folder, new_name)
        )