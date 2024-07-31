#!/bin/bash

# Define the user inputs
PROJECT_NAME="TestProject"
SWAP_VERSION="1.0"
FIRST_NAME="John"
LAST_NAME="Doe"
INSTITUTION="XYZ University"
EMAIL="john.doe@example.com"
FOLDER_NAME="TestProjectFolder"
COMMENT="No comments"

# Simulate the inputs
(
  echo "$PROJECT_NAME"
  echo "$SWAP_VERSION"
  echo "$FIRST_NAME"
  echo "$LAST_NAME"
  echo "$INSTITUTION"
  echo "$EMAIL"
  echo "$FOLDER_NAME"
  echo "$COMMENT"
) | pyswap init --script

# Check the result
if [ -f "$FOLDER_NAME/models/main.py" ]; then
  echo "Test passed: directories and main.py were created successfully."
  cat "$FOLDER_NAME/models/main.py"
else
  echo "Test failed: main.py was not created."
fi
