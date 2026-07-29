#!/bin/bash
pygbag --build main.py
cp custom_web/index.html build/web/index.html
cp -r custom_web/fonts build/web/fonts
echo "Rebuilt and reapplied custom index.html + fonts"
