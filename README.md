# ENOB Explorer

An interactive explorer for **ENOB (Effective Number of Bits)**: how a real ADC's
impairments — aperture jitter / phase noise, thermal (AWGN) noise, static
nonlinearity/distortion, and finite quantization — collapse into a single
*effective* resolution, expressed as the equivalent perfect ADC.

Move the sliders to impair a "real" ADC and watch its SINAD/ENOB drop in both the
time and frequency domains, next to an ideal, quantization-noise-only reference
whose SINAD matches by construction ("a perfect ADC of how many bits gives this
same performance?").

**Live app:** https://andrew-szajna-keysight.github.io/enob-explorer/voici/render/enob-explorer.html

The whole thing is a single notebook (`enob-explorer.ipynb`) rendered to a static,
client-side dashboard with [Voici](https://voici.readthedocs.io/) /
[JupyterLite](https://jupyterlite.readthedocs.io/) (Pyodide kernel) — there is no
server; all computation runs in the browser. The layout is responsive: a
two-column figure on the desktop that reflows to a single stacked column, with
full-width controls, on phones.

## Run / build locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                              # create the environment
uv run jupyter lab enob-explorer.ipynb              # edit / run interactively
uv run voici build --contents enob-explorer.ipynb   # build the static site into _output/
python -m http.server -d _output 8000               # serve the build at http://localhost:8000
```

Deployment is automated: pushing to `main` builds the Voici site and publishes it
to GitHub Pages (see `.github/workflows/`).

## License

No license is provided, so all rights are reserved by the author (see GitHub's
note on [no-license repositories](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#choosing-the-right-license)
and <https://choosealicense.com/no-permission/>). You're welcome to view the
deployed app, but the source is not licensed for reuse, modification, or
redistribution without permission.

## Author

Created by **Andrew Szajna**.

© 2026 Andrew Szajna. All rights reserved.
