# Contributing to AIQ CRM Insight Scout

Thank you for your interest in contributing to **AIQ CRM Insight Scout**! This hackathon project welcomes contributions to help master Agentic AI for CRM systems. Whether it's fixing bugs, adding features, or improving documentation, your help is appreciated.

## How to Contribute

1. **Fork the Repository**: Create your own fork of the project on GitHub.
2. **Create a Branch**: Make a new branch for your changes (e.g., `git checkout -b feature/new-feature`).
3. **Make Changes**: Implement your feature or fix, ensuring code follows the project's style (e.g., PEP 8 for Python).
4. **Test Locally**: Run `python app.py` and test via the Gradio UI at `http://localhost:8000/`.
5. **Commit Changes**: Use descriptive commit messages (e.g., `git commit -m "Add CCPA compliance query handling"`).
6. **Push to Fork**: `git push origin feature/new-feature`.
7. **Open Pull Request**: Submit a PR to the main repository, describing your changes and any relevant issues.

## Development Setup

Follow the [Installation](#installation) steps in README.md:
- Install dependencies: `pip install -r requirements.txt`
- Set up `.env` with `NVIDIA_API_KEY`
- Ensure `../data/` has all 9 markdown files
- Run `python app.py`

Test queries like "What is the due date for the xAI invoice?" to verify functionality.

## Code Style and Standards

- **Python**: Use PEP 8; tools like `black` and `flake8` for formatting/linting.
- **Modularity**: Prefer single-responsibility files (e.g., `agent_graph.py` for LangGraph logic).
- **Comments**: Document complex logic, e.g., FAISS indexing or NVIDIA API calls.
- **Error Handling**: Include try-except blocks for API timeouts and file loading.

## Reporting Issues

- Use GitHub Issues for bugs or feature requests.
- Provide details: Query example, error logs, expected vs. actual output.
- For security issues, see SECURITY.md.

## Pull Request Guidelines

- PRs must pass basic tests (e.g., app runs without errors).
- Reference related issues (e.g., "Fixes #123").
- Keep PRs focused; large changes should be split.

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

For questions, open an issue or contact the maintainer via GitHub.