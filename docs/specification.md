**Table of Contents**

-   [rescuerepo](#project-name-rescuerepo)
    -   [Introduction](#introduction)
    -   [Hypothetical usage](#usage)
    -   [Functional Requirements](#functional-requirements)
        -   [Architecture and Design](#architecture-and-design)
        -   [Developer](#developer)
        -   [User](#user)   
    -   [Non-functional Requirements](#non-functional-requirements)
    -   [Data Model](#data-model)
    -   [External interfaces](#external-interfaces)
    -   [Project structure](#structure)
    -   [Testing](#testing)
    -   [Deployment and Maintenance](#deployment-and-maintenance)

## Introduction

As already outlined in README here we intend to learn and apply the rules underlying regulatory element sequences using Stable Diffusion.

The architecture of RescueRepo intends to loosely adhere to the principles of Test-Driven Design (TDD),

Here are the main principles we strive to follow:

1. Write tests first: In TDD, you write a failing test before writing any production code. The test should be small, specific, and test only one aspect of the code.

2. Write the simplest code that passes the test: Once you've written the test, write the production code that will make the test pass. The code should be the simplest possible code that satisfies the test.

3. Refactor the code: Once the test has passed, you should refactor the code to improve its quality and maintainability. Refactoring means making changes to the code without changing its behavior.

4. Repeat the process: Once you've refactored the code, you should write another test and repeat the process.

5. Test everything that could possibly break: In TDD, you should write tests for all of the functionality that could potentially break. This includes boundary conditions, edge cases, and error conditions.

6. Use test automation: TDD relies on automated tests to verify that the code works as expected. Writing tests manually can be time-consuming and error-prone, so you should use test automation tools to write and run your tests.

7. Keep the feedback loop short: TDD is based on a short feedback loop, where you write a test, run it, and get immediate feedback on whether the code works as expected. This short feedback loop helps you catch errors early and makes it easier to debug problems.

## Hypothetical usage

TBD

## Functional Requirements

### Architecture and Design

TODO finish after initial refactoring is in place.

### Developer

TODO finish after initial refactoring is in place.

### User

TODO finish after initial refactoring is in place.

## Non-functional Requirements

TODO finish after initial refactoring is in place.


## Data Model

TODO finish after initial refactoring is in place.

## External interfaces

Hosted and exposed on Hugging face.

## Project structure

```
RescueRepo
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── Procfile
├── README.md
├── TERMS.md
├── assets
│   ├── images
│   │   ├── BioML_Hackathon_Blueprint.png
│   │   ├── codespace_screenshot.png
│   │   ├── example_codespaces.png
│   │   ├── initial_page.png
│   │   └── post_sign_in.png
│   └── notebooks
│       ├── Claude_100K_API_Exploration.ipynb
│       └── OpenAI_Bioinformatics_Tool_Embeddings.ipynb
├── backend
│   ├── __init__.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── few_shot_examples.py
│   │   ├── gh_client.py
│   │   ├── llm_utils.py
│   │   ├── prompts.py
│   │   └── tasks.py
│   ├── main.py
│   └── requirements.txt
├── build.sh
├── docs
│   ├── contributors.md
│   ├── images
│   │   ├── BioML_Hackathon_Blueprint.png
│   │   ├── codespace_screenshot.png
│   │   ├── example_codespaces.png
│   │   ├── initial_page.png
│   │   └── post_sign_in.png
│   ├── index.md
│   ├── reference
│   │   └── rescuerepo.md
│   └── specification.md
├── frontend
│   ├── README.md
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── index.css
│       ├── index.js
│       ├── logo.svg
│       ├── reportWebVitals.js
│       └── setupTests.js
├── mkdocs.yml
├── nextjs
│   ├── README.md
│   ├── app
│   │   ├── favicon.ico
│   │   ├── force.css
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components
│   │   ├── github
│   │   │   └── main.tsx
│   │   └── ui
│   │       ├── command.tsx
│   │       └── dialog.tsx
│   ├── lib
│   │   └── utils.ts
│   ├── next.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── postcss.config.js
│   ├── public
│   │   ├── next.svg
│   │   └── vercel.svg
│   ├── tailwind.config.js
│   └── tsconfig.json
├── render-test.yaml
├── requirements.txt
├── runtime.txt
├── secrets.sh
├── start_linux.sh
└── start_macos.sh

```

## Testing

reporescue will be tested using the [pytest](https://docs.pytest.org/en/stable/) framework.


## Deployment and Maintenance

reporescue will be distributed as a python package that can be installed and executed on any system with python version 3.10 or greater.
