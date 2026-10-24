# GitRE: Before Merging, Check Your Requirements - Supplemental Material

## Purpose

This appendix contains the project data, generated output files, and evaluation artifacts used in the NIER submission titled **"GitRE: Before Merging, Check Your Requirements"**. 

This work investigates requirements, issues, and the links between them. We present a dataset of seven projects, each consisting of requirements, issues, and the links between them. 

## File Tree

```text
root/
├── analysis-script.py 
├── dataset/ 
│   ├── matches/ 
│   │   └── project-og-matches.csv
│   └── org/ 
│       ├── project-og-issues.csv 
│       └── project-og-reqs.csv
├── gitRE-alpha-output/ 
│   ├── project-git-issues.csv 
│   ├── project-git-specs.csv 
│   └── project-git-sugg.csv
├── gitRE-k3-output/ 
│   ├── project-git-issues.csv 
│   ├── project-git-specs.csv 
│   └── project-git-sugg.csv 
├── claude-k3-output/ 
│   ├── project-git-issues.csv 
│   ├── project-git-specs.csv 
│   └── project-git-sugg.csv 
├── results-alpha/ 
│   ├── project-precision.csv 
│   ├── project-recall.csv 
│   └── project-missing-issues.csv 
├── results-K3/
│   ├── project-precision.csv
│   ├── project-recall.csv 
│   └── project-missing-issues.csv 
├── claude-conversation.md # claude prompt and response
└── readme.md # This file
```

The `project` can be any of `blit`, `cctns`, `spacefractions`, `warc`, `keepass` `gammaj` , or `peering`.

## Folder Descriptions

### `dataset/`
This is the primary source data directory. It contains the original source issue and requirement sets and the manually curated ground-truth matches.

- `dataset/org/` contains the original project data, including requirement files (`*-og-reqs.csv`) and issue files (`*-og-issues.csv`).
- `dataset/matches/` contains the oracle or ground-truth requirement-to-issue links (`*-og-matches.csv`).

### `gitRE-alpha-output/`
This folder holds the generated artifact files for the alpha algorithm experiment. Each project has three output files:

- `*-git-issues.csv`: issue IDs and titles
- `*-git-specs.csv`: specification IDs and titles
- `*-git-sugg.csv`: suggested links between issue IDs and specification IDs

### `gitRE-k3-output/`
This folder mirrors the alpha output but contains data produced for the K3 algorithm.

### `claude-k3-output/`
This folder also mirrors the alpha/k3 output, but contains data produced from the Claude-based algorithm.

### `results-alpha/` and `results-K3/`
These directories contain evaluation summaries generated from the algorithm output files. Outputs include:

- `*-precision.csv`: per-issue precision values
- `*-recall.csv`: per-issue recall values
- `*-missing-issues.csv`: issues with no specification matches in the ground truth

### `analysis-script.py`
This script is used to map original IDs from the project datasets to generated IDs and to compute precision and recall against the ground-truth match files.

## Claude Suggested Requirements Generation Summary

We used the [free web version of Claude](https://claude.ai/). We identified that Claude Sonnet 5.5 uses clustering, not cosine similarity and embeddings, to make associations, and used it to generate suggested requirements. We curated one prompt to generate suggestions for our seven projects, to ensure that the same process was used for generating suggestions for all. For each of our seven projects, we provided a CSV of the project’s requirements and their ids and a CSV of the project’s issues and their ids, and gave detailed instructions on which issues and requirements files were to be compared. We asked Claude to compare the title and description of each requirement to the title and description of each issue and then determine the three most relevant requirements for each issue. For each project, we instructed Claude to put its results in a CSV where each row contains a suggested requirement id and an issue id. Note that our analysis script expects the suggestion CSVs to have an additional ‘id’ column due to the format of the suggestion CSVs from GitRe, so this column was manually added after the fact. For more insight into Claude’s comparison, we asked for it to describe the process it took to link the requirements to issues. The full conversation can be found in the `claude-conversation.md` file. 

## License
This work is licensed under a [Creative Commons Attribution-NonCommercial-No Derivative Works 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).
