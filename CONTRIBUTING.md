# Contributing to AI File Organizer

Thank you for your interest in contributing to AI File Organizer! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## How to Contribute

1. **Fork the Repository**
   - Fork the repository to your GitHub account
   - Clone your fork locally: `git clone https://github.com/yourusername/ai-file-organizer.git`

2. **Create a Branch**
   - Create a branch for your changes: `git checkout -b feature/your-feature-name`
   - Use descriptive branch names (e.g., `feature/add-file-type-detection`)

3. **Make Your Changes**
   - Follow the coding style of the project
   - Add or update tests as needed
   - Update documentation to reflect your changes

4. **Test Your Changes**
   - Run all tests: `python -m pytest`
   - Ensure all tests pass
   - Test your changes thoroughly

5. **Commit Your Changes**
   - Use clear and descriptive commit messages
   - Reference any relevant issues
   - Example: `git commit -m "Add file type detection for audio files #123"`

6. **Submit a Pull Request**
   - Push to your fork: `git push origin feature/your-feature-name`
   - Create a Pull Request from your fork to our main repository
   - Describe your changes in detail
   - Link any related issues

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

## Testing

- Write tests for new features
- Update existing tests when modifying features
- Aim for high test coverage
- Use pytest for testing

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions and classes
- Update installation and usage instructions if needed
- Document any new dependencies

## Pull Request Process

1. Ensure all tests pass
2. Update documentation as needed
3. Add yourself to CONTRIBUTORS.md if not already there
4. Request review from maintainers
5. Address review feedback

## Getting Help

- Create an issue for bugs or feature requests
- Join our discussions for general questions
- Contact maintainers for sensitive issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 