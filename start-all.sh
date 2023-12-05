#!/bin/bash

# Chemin vers l'environnement virtuel
VENV_PATH="brightnessaiv2"

# Activation de l'environnement virtuel
source "$VENV_PATH/bin/activate"

# Lancement de Gunicorn avec la configuration spécifique
gunicorn --bind 0.0.0.0:8000 -w 4 streaming_api:app --timeout 1200 --daemon --access-logfile docs/access.log --error-logfile docs/error.log --capture-output

gunicorn --bind 0.0.0.0:8001 -w 4 transformers_api:app --timeout 7200 --daemon --access-logfile access.log --error-logfile docs/error.log --capture-output

gunicorn --bind 0.0.0.0:8002 -w 4 alter_brain_api:app --timeout 1200 --daemon --access-logfile docs/access.log --error-logfile docs/error.log --capture-output

# Désactivation de l'environnement virtuel (facultatif)
deactivate
