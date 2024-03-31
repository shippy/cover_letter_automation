[![Lint and Test](https://github.com/shippy/cover_letter_automation/actions/workflows/test.yml/badge.svg)](https://github.com/shippy/cover_letter_automation/actions)

# Cover Letter Automation

A Python package for ingesting job descriptions & resumes, and crafting cover letters that use the latter to satisfy the former.

## 🚀 Using

While the package is in theory pip-installable, it's not yet on PyPI. For now, you can clone the
repo and run the following:

```bash
git clone https://github.com/shippy/cover_letter_automation.git
cd cover_letter_automation
poetry install
```

Then, you should place your `resume.json` ([JSON Resume](https://jsonresume.org), although in
principle it doesn't have to have that exact schema) in `resume/` and your job descriptions in
`jd/`. You can then run the following:

```bash
poetry run python init_session.py --resume resume/$RESUME_NAME.json --jd jd/$JD_NAME.md
# In theory, if you've placed your resume at resume/resume.json, you can omit that argument
```

Currently, due to the slightly ad-hoc nature of the agents, you'll need to run the above command for
each job description you want to generate a cover letter for. The cover letters will be placed in
`cover_letters/`.


## 🧑‍💻 Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Install Docker</summary>

1. Go to [Docker](https://www.docker.com/get-started), download and install docker.
2. [Configure Docker to use the BuildKit build system](https://docs.docker.com/build/buildkit/#getting-started). On macOS and Windows, BuildKit is enabled by default in Docker Desktop.

</details>

<details>
<summary>2. Install VS Code</summary>

Go to [VS Code](https://code.visualstudio.com/), download and install VS Code.
</details>


</details>

#### 1. Open DevContainer with VS Code
Open this repository with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.

The following commands can be used inside a DevContainer.

#### 2. Run linters
```bash
poe lint
```

#### 3. Run tests
```bash
poe test
```

#### 4. Update poetry lock file
```bash
poetry lock --no-update
```

#### 5. Add dependencies and remove them if not needed
```bash
poetry add package
poetry remove package
# or remove the package from the pyproject.toml file and run
poetry install --sync
```

## Credits

<details>
<summary>️⚡️ Scaffolded with Copier.</summary>

See [Poetry Copier](https://github.com/lukin0110/poetry-copier/).

🛠️ [Open an issue](https://github.com/lukin0110/poetry-copier/issues/new) if you have any questions or suggestions.

See how to develop with [PyCharm or any other IDE](https://github.com/lukin0110/poetry-copier/tree/main/docs/ide.md).
</details>