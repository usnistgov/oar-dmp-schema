import sys
import os
import json
from pathlib import Path
from urllib.parse import urljoin

from jsonschema import validate, exceptions, Draft202012Validator

with open('dmp-schema.json') as json_file:
  dmp_schema = json.load(json_file)

instance_filename = 'test-record.json'
    
with open(instance_filename) as instance_file:
  document = json.load(instance_file)

try:
  validate(instance=document, schema=dmp_schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
  print("Valid")
except exceptions.ValidationError as e:
  print("Validation failed!")
  print (f"Error message: {e.message}")