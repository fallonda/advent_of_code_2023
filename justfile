default:
    just --list

# Activate python virtual environment
activate_venv:
    ./env/bin/activate

# Setup venv
setup_venv:
    python3 -m venv env

# Install from pip requirements.txt
pip_install_req:
    pip install -r requirements.txt