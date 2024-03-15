#!/bin/bash
cd Flask
pip install -r requirements.txt
chmod +w users.csv
chmod +w scheduled_practices.csv
python app.py
