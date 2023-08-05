# CLIME Issue Density

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6478225.svg)](https://doi.org/10.5281/zenodo.6478225)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-issue-density/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-issue-density/actions/workflows/release.yml)

> A tool to calculate the issue density of a Git repository by analyzing the issues of a project in it's issue tracker

## Table of Contents

- [CLIME Issue Density](#clime-issue-density)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Issue Density Project is a `python` tool to calculate the issue density of a GitHub repository. It is reliant upon the output of the [GitHub Issue](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues) and [Git Commits](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc) tools.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip clime-metrics`
- `pip install --upgrade pip clime-issue-density`

### Command Line Arguements

`clime-issue-density-compute -h`

``` shell
usage: CLIME Issue Density [-h] [-c COMMITS] [-i ISSUES] [-o OUTPUT] [-v]

A tool to calculate the issue density of a repository

options:
  -h, --help            show this help message and exit
  -c COMMITS, --commits COMMITS
                        Commits JSON file. DEFAULT: ./commits_loc.json
  -i ISSUES, --issues ISSUES
                        Issues JSON file. DEFAULT: ./github_issues.json
  -o OUTPUT, --output OUTPUT
                        Output JSON file. DEFAULT: ./issue_density.json
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Matthew Hyatt, Sohini Thota, George K.
Thiruvathukal
```

`clime-issue-density-graph -h`

``` shell
usage: CLIME Issue Density Grapher [-h] [-i INPUT] [-o OUTPUT] [--type TYPE]
                                   [--title TITLE] [--x-label X_LABEL]
                                   [--y-label Y_LABEL]
                                   [--stylesheet STYLESHEET] [-v]

A tool to graph the issue density of a repository

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON export from CLIME GitHub Issue Density Compute.
                        DEFAULT: ./issue_density.json
  -o OUTPUT, --output OUTPUT
                        Filename of the graph. DEFAULT: ./issue_density.pdf
  --type TYPE           Type of figure to plot. DEFAULT: line
  --title TITLE         Title of the figure. DEFAULT: ""
  --x-label X_LABEL     X axis label of the figure. DEFAULT: ""
  --y-label Y_LABEL     Y axis label of the figure. DEFAULT: ""
  --stylesheet STYLESHEET
                        Filepath of matplotlib stylesheet to use. DEFAULT: ""
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Matthew Hyatt, Sohini Thota, George K.
Thiruvathukal
```
