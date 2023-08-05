# CLIME: Command Line Metrics Tool

> A complete installer for CLIME

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6477789.svg)](https://doi.org/10.5281/zenodo.6477789)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime/actions/workflows/release.yml)

## Table of Contents

- [CLIME: Command Line Metrics Tool](#clime-command-line-metrics-tool)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
    - [Shell Software](#shell-software)
  - [Bundled Projects](#bundled-projects)

## About

The Software Systems Laboratory (SSL) CLIME project is a collection of `python` tools that can be used on any Git repository to generate longitudinal graphs of classical process metrics.

You can install the entirety of the CLIME project from Pypi with `pip install --upgrade pip clime-metrics`.

### Licensing

These tools can be modified by outside teams or individuals for usage of their own personal projects.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project and the greater SSL CLIME project, the following dependencies are **required**:

### Operating System

All tools developed for the greater SSL CLIME project **target** Mac OS and Linux. CLIME is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

### Shell Software

The following software **is required** to run the tools:

- `cloc`
- `git`
- `python 3.9.6` or newer
- `sloccount`

The following software **is optional** to run the tools:

- `jq`
- `parallel`
- `Parallel::ForkManager` Perl package

## Bundled Projects

This projects bundles the following `python` projects into one `pip` installable:

- [CLIME Bus Factor](https://github.com/SoftwareSystemsLaboratory/clime-git-bus-factor)
- [CLIME Commits LOC](https://github.com/SoftwareSystemsLaboratory/clime-git-commits-loc)
- [CLIME Productivity](https://github.com/SoftwareSystemsLaboratory/clime-git-productivity)
- [CLIME Issues](https://github.com/SoftwareSystemsLaboratory/clime-github-issues)
- [CLIME Issue Density](https://github.com/SoftwareSystemsLaboratory/clime-github-issue-density)
- [CLIME Issue Spoilage](https://github.com/SoftwareSystemsLaboratory/clime-github-issue-spoilage)
- [CLIME Repository Searcher](https://github.com/SoftwareSystemsLaboratory/clime-github-repository-searcher)
- [CLIME JSON Converter](https://github.com/SoftwareSystemsLaboratory/clime-json-converter)
- [CLIME Badges](https://github.com/SoftwareSystemsLaboratory/clime-badges)
