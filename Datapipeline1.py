import pandas as pd
import json
import logging
import os
from cryptography.fernet import Fernet
from sklearn.model_Selection import train_test_split
from sklearn.svm import SVC

logging.basicConfig(filename="audit_log.txt", level=logging.INFO, format=)