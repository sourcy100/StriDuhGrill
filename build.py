
# Compiling thing

import os

commands = [
    'python -m PyInstaller --onefile Game.py',
    'rm -rf ./build', 
    'mv ./dist/* .',
    'rm -rf ./dist',
    'rm -rf Game.spec'
]

for command in commands:
    os.system(command)