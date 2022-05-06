# Main operations with Command line interface (CLI).
# CLI application
import os
import json
import tempfile
import warnings
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
#import tensorflow 
import typer
from feast import FeatureStore
from numpyencoder import NumpyEncoder
from optuna.integration.mlflow import MLflowCallback

from orchestrator import mlflow
from babushka import data, models, predict, train, utils 

# Ignore warning
#warnings.filterwarnings("ignore")

# Typer CLI app
app = typer.Typer()

@app.command()
def download_auxiliary_data():
    print("test")

@app.command()
def trigger_orchestrator():
    os.system("export ENV_NAME=test")
    os.system("export REGION=us-central1")
    os.system("export FILE=sample.py")
    os.system("gcloud composer environments storage dags import \
    --environment $ENV_NAME --location $REGION --source $FILE")

    pass

@app.command()
def compute_feature():
    pass

@app.command()
def trainer():
    pass

@app.command()
def load_artifacts():
    model = models.load_model()
    pass