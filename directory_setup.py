import os

# Define the directory structure
directories = [
    'src/solo_plai/core',
    'src/solo_plai/data',
    'src/solo_plai/agent',
    'src/solo_plai/api/routes',
    'src/solo_plai/game',
    'src/solo_plai/utils',
    'tests/test_api',
    'tests/test_game',
    'tests/test_agent',
    '.github/workflows',
    'alembic'
]

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Define the files to be created
files = [
    'src/solo_plai/core/__init__.py',
    'src/solo_plai/data/__init__.py',
    'src/solo_plai/agent/__init__.py',
    'src/solo_plai/api/__init__.py',
    'src/solo_plai/api/routes/__init__.py',  # Added routes init file
    'src/solo_plai/game/__init__.py',
    'src/solo_plai/utils/__init__.py',
    'src/solo_plai/__init__.py',
    'src/solo_plai/main.py',
    'tests/__init__.py',
    'tests/conftest.py',
    'README.md',
    '.env.example',
    '.gitignore'  # Added gitignore instead of requirements.txt
]

# Create files
for file in files:
    with open(file, 'w') as f:
        # Add basic content to .gitignore
        if file == '.gitignore':
            f.write(".venv/\n__pycache__/\n*.py[cod]\n*$py.class\n")
