#!/bin/bash
pip install --no-index --find-links=. -r requirements.txt
echo "Installation complete. Press [Enter] to exit..."
read -r
