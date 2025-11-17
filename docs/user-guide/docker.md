# Docker

Docker provides a consistent environment for running pySWAP across different operating systems. This ensures that pySWAP runs identically regardless of your local system configuration.

## Why Docker?

- **Cross-platform compatibility**: Run pySWAP on any system that supports Docker
- **Consistent environment**: Same setup for all team members
- **Isolated execution**: No conflicts with your local system
- **Easy deployment**: Reproducible environment setup
- **Platform independence**: Avoid system-specific compatibility issues

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- Basic knowledge of Docker commands

## Common use cases

### Platform compatibility

Docker is useful when you encounter system-specific issues such as:

- **Architecture mismatches**: SWAP420 is compiled for Linux x86-64
- **Missing dependencies**: System libraries not available on your platform
- **Version conflicts**: Different system library versions
- **Environment differences**: Inconsistent behavior across systems

Docker provides a standardized Linux environment where pySWAP and SWAP420 can run consistently.

## Quick start

### 1. Build the image

Navigate to your pySWAP project directory and build the Docker image:

```shell
docker build -t pyswap .
```

This creates an image named `pyswap` with Python 3.11, pySWAP, and SWAP420 Linux executable.

### 2. Run with volume mounting

For development, mount your local workspace to the container:

```shell
docker run -it --rm -v "$PWD":/workspace pyswap
```

**Command breakdown:**

- `-it`: Interactive terminal
- `--rm`: Remove container after stopping
- `-v "$PWD":/workspace`: Mount current directory to `/workspace` in container

### 3. Run your scripts

With volume mounting, you can:

- **Edit code locally** using your preferred editor (VS Code, PyCharm, etc.)
- **Run scripts immediately** in the container: `python your-script.py`
- **Iterate quickly** - changes are instantly available without rebuilding
- **Maintain your workflow** with Git and other tools on your local system

```shell
python your-script.py
```

### 4. Shutdown Docker

When you're finished with your analysis, you can exit the container:

**If you're inside the container:**

```bash
exit
```

**If you're in a different terminal and want to stop a running container:**

```shell
# List running containers and find pySWAP
docker ps

# Look for a container with:
# - Image: pyswap
# - Name: usually auto-generated
# - Status: Up

# Stop the specific pySWAP container
docker stop <container_name_or_id>
```

## Alternative Usage Patterns

For quick testing without entering the container:

```shell
docker run --rm -v "$PWD":/workspace pyswap python your-script.py
```

## Next Steps

- Try running the [tutorials](/tutorials/) in Docker
- Explore the [user guide](/user-guide/) for more pySWAP features
- Check the [contributing guidelines](/contributing/) if you want to help improve Docker support
