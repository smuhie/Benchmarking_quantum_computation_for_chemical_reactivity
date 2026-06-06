# Reaction observable benchmarks for useful quantum computation in chemical reactivity

This repository contains the Python code used to generate Figures 1–4 for the manuscript:

**Reaction observable benchmarks for useful quantum computation in chemical reactivity**

## Repository contents

- `generate_all_figures.py` — reproduces all four manuscript figures.
- `src/figure1.py`–`src/figure4.py` — individual figure-generation scripts.
- `notebooks/Benchmarking_quantum_computation_for_chemical_reactivity.ipynb` — original notebook used during figure development.
- `figures/` — exported final figure files in PDF and PNG formats.
- `requirements.txt` — Python package requirements.

## Requirements

The figures were generated with Python 3 and require:

- matplotlib
- numpy

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Reproducing the figures

From the repository root, run:

```bash
python generate_all_figures.py
```

The output files will be written to:

```text
figures/
```

## Data availability

No primary datasets are required to generate these schematic figures. All figure content is encoded directly in the figure-generation scripts.

## Notes

The scripts are derived from the original notebook but have been standardized so that all four figures are exported automatically with manuscript-ready filenames.

## License

Code in this repository is released under the MIT License. Figure reuse should also follow the license and citation terms of the associated manuscript.
