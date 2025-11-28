#!/bin/bash
docker run --rm -v $(pwd):/workspace -w /workspace openjournals/inara:latest -o pdf paper/paper.md