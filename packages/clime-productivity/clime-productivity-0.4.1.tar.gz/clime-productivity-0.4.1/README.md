# CLIME Productivity

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6480656.svg)](https://doi.org/10.5281/zenodo.6480656)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-productivity/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-productivity/actions/workflows/release.yml)

> A tool to calculate the productivity of a Git repository

## Table of Contents

- [CLIME Productivity](#clime-productivity)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Shell Commands](#shell-commands)

## About

The Software Systems Laboratory (SSL) CLIME Productivity project is a tool to calculate the productivity of a Git repository.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install this tool with one of the following one liners:

- `pip install --upgrade pip clime-meta`
- `pip install --upgrade pip clime-productivity`

### Shell Commands

`clime-productivity-compute -h`

``` shell
usage: CLIME Repository Productivity Calculator [-h] [-i INPUT] [-o OUTPUT]

A tool to calculate the productivity of a Git repository where productivity is
defined as: |ΔLOC| / (Repository Age)

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Commits JSON file. DEFAULT: ./commits_loc.json
  -o OUTPUT, --output OUTPUT
                        Output JSON file. DEFAULT: ./productivity.json

Author(s): Nicholas M. Synovic, Matthew Hyatt, George K. Thiruvathukal
```

`clime-productivity-graph -h`

``` shell
usage: CLIME Productivity Grapher [-h] [-i INPUT] [-o OUTPUT] [--type TYPE]
                                  [--title TITLE] [--x-label X_LABEL]
                                  [--y-label Y_LABEL]
                                  [--stylesheet STYLESHEET] [-v]

A tool to graph the productivity of a repository

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON export from CLIME GitHub Issue Density Compute.
                        DEFAULT: ./productivity.json
  -o OUTPUT, --output OUTPUT
                        Filename of the graph. DEFAULT: ./productivity.pdf
  --type TYPE           Type of figure to plot. DEFAULT: line
  --title TITLE         Title of the figure. DEFAULT: ""
  --x-label X_LABEL     X axis label of the figure. DEFAULT: ""
  --y-label Y_LABEL     Y axis label of the figure. DEFAULT: ""
  --stylesheet STYLESHEET
                        Filepath of matplotlib stylesheet to use. DEFAULT: ""
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Matthew Hyatt, George K. Thiruvathukal
```
