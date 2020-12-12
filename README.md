# Advent of Code

My solutions to https://adventofcode.com.

## Setup

Set up Conda environment (after installing Conda/Miniconda):
```bash
conda create --name aoc python=3.7
conda activate aoc
```

Install Jupyter notebook as follows ([link](https://jupyter.org/install)):
```bash
conda install -c conda-forge notebook
```

Run Jupyter notebook by:
```bash
jupyter notebook
```

Enable Conda environment in Jupyter notebook guide ([link]([https://medium.com/@nrk25693/how-to-add-your-conda-environment-to-your-jupyter-notebook-in-just-4-steps-abeab8b8d084)):

```bash
conda install -c anaconda ipykernel
python -m ipykernel install --user --name=aoc
```