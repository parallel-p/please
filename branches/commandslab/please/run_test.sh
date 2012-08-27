#!/bin/bash
find . -name "*_test.py" -type f | sed "s|\./|python3 -m|g" | sed "s|/|.|g" | sed "s/\.py//g" | bash

