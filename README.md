<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>ITN</h1>
<h3> A Python Module for cleaning P3B template, tracking and validating data during data collection and creating random location to revisit after implementation </h3>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=flat-square&logo=Jupyter&logoColor=white" alt="Jupyter" />
<img src="https://img.shields.io/badge/Qgis-589632.svg?style=flat-square&logo=Qgis&logoColor=white" alt="Qgis" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas" />
</p>
<img src="https://img.shields.io/github/license/Mrsatatima/p3b?style=flat-square&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/Mrsatatima/p3b?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/Mrsatatima/p3b?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/Mrsatatima/p3b?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running p3b](#-running-p3b)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

A module mostly focus on cleaning the p3b template and turn it to a format you can use for various data analysis. It then provides you with tools you can use to:
- create 8 random settlements google directions links per LGA for post-implementation revisits to confirm the accuracy of distributed ITNs 
- track and verifying the accuracy of captured points during data collection
- Matching of settlements from GRID3 database to settlements on the p3b to add location to them

---

## 📦 Features

### Cleaning of p3b template
- The p3b template is an excel file with various merger cell which makes it hard to use it for data analysis see image below

<p align=center>
<img src= "/images/p3b_header.png"/>
<img src= "/images/p3b_cells.png"/>
</p>

- This modules then unmerges all cells, removes unwanted columns and rows, set the right and populate a ward and DH for each settlement see image below
<p align=center>
<img src= /images/p3b_cells_populated.png/>
</p>

### Creating 8 random settlement google directions per LGA for post-implementation revisits
- Normally after every ITN campaign there is a post implementation activity which involves rapid assesment of  ITN distribution campaign to determine ITN coverage, ownership, access, hanging rate etc.
- To do this random locations are selected  form each LGA for visit. Cluster selection (8) from from each LGA is done  using Probability Proportional to Size (PPS)
- Giving the large number of LGAs it takes time to create this cluster
- This module provides a tool to create this location and assign a google map direction
<div>
<p align=center> How it is done manually </p>
<ol>
   <li>sort wards by thier population in ascending order</li>
   <li>Create a cumulative frequency</li>
   <li>set PPES interval</li>
   <li>set a random starting point</li>
   <li>create cluster increament the starting point with the interval</li>
   <li>attach each cluster to the cummulative frequency range they fall in</li>
   <li>Then manually get a random settlement direction from each cluster</li>
</ol>
<img src="/images/random_cluster_1-7.png" />
<img src="/images/random_cluster_8.png" />
</div>





---


## 📂 Repository Structure

```sh
└── ITN/
    ├── Cluster/
    │   ├── cluster.py
    │   └── main.py
    ├── geo_script.py
    ├── helper.py
    ├── main.py
    ├── Matching/
    │   ├── main.py
    │   └── matching.py
    ├── notebook.ipynb
    ├── p3b.py
    ├── requirements.txt
    └── Tracker/
        ├── main.py
        └── tracker.py

```

---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                                                             | Summary       |
| ---                                                                              | ---           |
| [geo_script.py](https://github.com/Mrsatatima/p3b/blob/main/geo_script.py)       | ► INSERT-TEXT |
| [helper.py](https://github.com/Mrsatatima/p3b/blob/main/helper.py)               | ► INSERT-TEXT |
| [main.py](https://github.com/Mrsatatima/p3b/blob/main/main.py)                   | ► INSERT-TEXT |
| [notebook.ipynb](https://github.com/Mrsatatima/p3b/blob/main/notebook.ipynb)     | ► INSERT-TEXT |
| [p3b.py](https://github.com/Mrsatatima/p3b/blob/main/p3b.py)                     | ► INSERT-TEXT |
| [requirements.txt](https://github.com/Mrsatatima/p3b/blob/main/requirements.txt) | ► INSERT-TEXT |
| [cluster.py](https://github.com/Mrsatatima/p3b/blob/main/Cluster\cluster.py)     | ► INSERT-TEXT |
| [main.py](https://github.com/Mrsatatima/p3b/blob/main/Cluster\main.py)           | ► INSERT-TEXT |
| [main.py](https://github.com/Mrsatatima/p3b/blob/main/Matching\main.py)          | ► INSERT-TEXT |
| [matching.py](https://github.com/Mrsatatima/p3b/blob/main/Matching\matching.py)  | ► INSERT-TEXT |
| [main.py](https://github.com/Mrsatatima/p3b/blob/main/Tracker\main.py)           | ► INSERT-TEXT |
| [tracker.py](https://github.com/Mrsatatima/p3b/blob/main/Tracker\tracker.py)     | ► INSERT-TEXT |

</details>

---

## 🚀 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

`- ℹ️ Dependency 1`

`- ℹ️ Dependency 2`

`- ℹ️ ...`

### 🔧 Installation

1. Clone the p3b repository:
```sh
git clone https://github.com/Mrsatatima/p3b.git
```

2. Change to the project directory:
```sh
cd p3b
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Running p3b

```sh
python main.py
```

### 🧪 Tests
```sh
pytest
```

---


## 🛣 Project Roadmap

> - [X] `ℹ️  Task 1: Implement X`
> - [ ] `ℹ️  Task 2: Implement Y`
> - [ ] `ℹ️ ...`


---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/Mrsatatima/p3b/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Mrsatatima/p3b/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/Mrsatatima/p3b/issues)**: Submit bugs found or log feature requests for MRSATATIMA.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License


This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 👏 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#Top)

---

