# Makefile


Make file is particularily useful when a certain workflow, for example for testing code or docs has to be repeatadly executed. It allows you to define a set of tasks that can be run with simple commands, e.g., `make <some-command-name>`. In this project, the Makefile provides several useful options:

- **test-hupsel**: Installs the poetry environment and pre-commit hooks, then runs a specific test case.
- **testcheck**: Runs code quality tools in a test configuration, including checking the Poetry lock file, linting code, performing static type checking, and checking for obsolete dependencies. Saves the results from the QC tools to log files.
- **check**: Similar to `testcheck`, but runs the tools without saving the output to log files.
- **test**: Runs the test suite with pytest, including coverage reporting.
- **build**: Cleans build artifacts and creates a wheel file using Poetry.
- **clean-build**: Removes the `dist` directory to clean up build artifacts.
- **publish**: Publishes a release to PyPI, with a dry run first to ensure everything is set up correctly.
- **build-and-publish**: Combines the build and publish steps into one command.
- **docs-test**: Tests if the documentation can be built without warnings or errors.
- **docs**: Builds and serves the documentation locally.
- **help**: Lists all available make commands with descriptions.

These commands are also used to simplify CI workflows in GitHub. You are more than welcome to define more commands when you contribute to the project.