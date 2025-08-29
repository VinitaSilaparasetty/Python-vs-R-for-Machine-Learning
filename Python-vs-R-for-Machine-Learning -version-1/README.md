<div class="column">
    <img alt="GitHub" src="https://img.shields.io/badge/Reviewed_by-Oxford_Academic-blue.svg">
    <img alt="GitHub" src="https://img.shields.io/badge/License-MIT-blue.svg">
    <img src="https://doi.org/10.5281/zenodo.16946994.svg" alt="DOI"></a>
    

#### *Note: This paper was presented at the International Conference on Security conference, where it won the Best Paper Award. It is not intended as groundbreaking ML research, but as an early exploration of the Python vs R debate from a security perspective. While the approach simplifies security (which depends more on dependencies and coding practices than language choice), I keep it here as part of my growth journey and for its teaching value.*

# Python vs R for Machine Learning

The paper compares Python and R as the dominant languages for machine learning, focusing on security and reproducibility.

*Disclaimer: Results may vary slightly by machine, network, and mirror availability.*

## Best Paper Award Winner

![Alt text](https://raw.githubusercontent.com/VinitaSilaparasetty/Python-vs-R-for-Machine-Learning/master/pythonvsr.JPG)

### Verdict

> "This paper is of relevance for teaching purposes." - Oxford Academic, The Computer Journal, Section C: Computational Intelligence, Machine Learning and Data Analytics 

## Contents
- `paper/` — LaTeX source.
- `figures/` — PNGs and generators.
- `code/py/` — Python demos, reproducibility harness, and security test suite.
- `code/py/artifacts/` — auto-generated pickled files for the security tests.
- `code/r/` — R demos and reproducibility harness.
- `code/notebooks/jupyter_trust_demo/` — Jupyter trust illustration.
- `code/secrets/` — simple secrets-leak check.

## Prerequisites
- Python 3.6 with `pipenv==11.10.1` (or similar 2018-era) and `pip`  
  (the security test suite runs with stdlib only, no extra packages needed)
- R 3.4 or 3.5 with packages `checkpoint`, `tidyverse`, `caret`, `rmarkdown`
- LaTeX (`latexmk`, `pdflatex`) if building the paper
- Git (for the secrets-leak check)

## Quick start

### 1) a) Python: unsafe serialization demo
```bash
cd code/py
python generate_malicious_pickle.py
python deserialization_test.py   # Demonstrates why untrusted pickle is unsafe
```

### 1) b) Python: full security test suite (T1–T7)
```bash
cd code/py
python run_security_tests.py
```

### 2) a) R: unsafe serialization demo
```r
cd code\r
Rscript generate_malicious_rds.R
Rscript deserialization_test.R
```
### Troubleshooting
```r
"C:\Program Files\R\R-3.5.0\bin\Rscript.exe" generate_malicious_rds.R
"C:\Program Files\R\R-3.5.0\bin\Rscript.exe" deserialization_test.R
```
### 2) b) R: full security test suite (T1–T6)
```r
cd code\r
"C:\Program Files\R\R-3.5.0\bin\Rscript.exe" run_security_tests.R
```

### 3) Reproducibility harnesses
#### Python (Pipenv)
```bash
cd code/py/reproducibility
chmod +x run_rebuilds.sh
./run_rebuilds.sh
```
### Troubleshooting

Ensure bash is installed then run:

```bash
bash run_rebuilds.sh
```
If this doesn't work use the run_rebuilds.bat instead.

```bat
run_rebuilds.bat
```

#### R (checkpoint snapshot 2018-04-01)
```r
setwd("code/r/reproducibility")
Rscript checkpoint_rebuild.R
```
#### Troubleshooting
```r
cd code\r\reproducibility
"C:\Program Files\R\R-3.5.0\bin\Rscript.exe" checkpoint_rebuild.R
```

### 4) Notebook trust illustration

#### Python
```bash
cd code/notebooks/jupyter_trust_demo
jupyter notebook
```
#### R
```r
"C:\Program Files\R\R-3.5.0\bin\Rscript.exe" -e "rmarkdown::render('code/notebooks/untrusted_demo.Rmd')"
```

### 5) Secrets leak check
```bash
cd code/secrets
chmod +x leak_check.sh
./leak_check.sh
```
### Troubleshooting

Ensure bash is installed then run:

```bash
bash leak_check.sh
```
If this doesn't work use the run_rebuilds.bat instead.

```bat
leak_check.bat
```

### Safety note
```yaml
The serialization demos execute benign commands to illustrate risk. Never load untrusted serialized files in real systems.
```


