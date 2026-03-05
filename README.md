# Behavioural Biases in Finance — Quarto Website

A Quarto-based website cataloguing behavioural biases in financial decision-making, with cross-linked examples and tag-based filtering. Hosted on GitHub Pages.

---

## Project Structure

```
.
├── _quarto.yml              # Site configuration (navbar, theme, search)
├── _variables.yml           # Site-wide variables
├── custom.scss              # Custom styles (hero search, cards, chips)
├── references.bib           # BibTeX bibliography
├── index.qmd                # Home page with hero search bar
├── biases.qmd               # Master listing with filter UI
├── about.qmd                # About page
│
├── biases/
│   ├── heuristics.qmd       # Category listing: Heuristics
│   ├── choices.qmd          # Category listing: Choices & Framing
│   ├── prospect-theory.qmd  # Category listing: Prospect Theory
│   ├── social.qmd           # Category listing: Social Factors
│   │
│   ├── attention-bias.qmd
│   ├── availability-heuristic.qmd
│   ├── hindsight-bias.qmd
│   ├── ... (one .qmd per bias)
│
└── images/                  # All images and Python plot scripts
```

---

## Adding a New Bias

1. Create `biases/your-bias-name.qmd`
2. Set the YAML front matter:
   ```yaml
   ---
   title: "Your Bias Name"
   description: "One-sentence summary for the listing page."
   categories: [heuristics]   # one or more of: heuristics, choices, prospect-theory, social
   ---
   ```
3. Write the content using the standard template (header badge, definition, examples callout, "Also relates to" block)
4. Add cross-links in related bias pages

---

## Local Development

### Prerequisites

- [Quarto ≥ 1.4](https://quarto.org/docs/get-started/)
- Python ≥ 3.10 with `matplotlib`, `numpy`, `pandas`, `jupyter`

### Commands

```bash
# Preview site locally with live reload
quarto preview

# Render to /docs (for GitHub Pages)
quarto render
```

---

## GitHub Pages Deployment

### One-time setup

1. Push this repository to GitHub
2. Go to **Settings → Pages**
3. Set **Source** to **GitHub Actions**
4. Trigger the workflow via a push to `main`, or manually via **Actions → Run workflow**

The GitHub Actions workflow (`.github/workflows/publish.yml`) will:
- Install Quarto and Python
- Run `quarto render` (outputs to `/docs`)
- Deploy `/docs` to GitHub Pages

### Images

Place all images in the `images/` folder. Python-generated plots should be `.py` scripts in `images/` called via `%run images/script-name.py` in code cells.

---

## SCSS Customisation

Key classes defined in `custom.scss`:

| Class | Purpose |
|---|---|
| `.hero-section` | Blue gradient hero banner on home page |
| `.hero-search` | Centres the Quarto search widget inside the hero |
| `.bias-grid` / `.bias-card` | Responsive card grid for category overview |
| `.tag-chip` + `.tag-*` | Coloured category pills |
| `.also-relates` | Cross-link block at bottom of each bias page |

---

## License

Content is original. Code is MIT licensed.
