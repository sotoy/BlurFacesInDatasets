#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Run the second Python script
python count_faces.py "$@" before

# Blur the faces
python detect_and_blur.py "$@"

# Run the second Python script
python count_faces.py "$@" after
