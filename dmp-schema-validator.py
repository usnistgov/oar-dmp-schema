import sys
import os
import json
from pathlib import Path
from urllib.parse import urljoin

from jsonschema import validate, exceptions, Draft202012Validator

dmp_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema#",
  "id": "https://example.com/mids-dmp.schema",
  "title":"NIST MIDAS Data Management Plan record",
  "type":"object",
  "properties" : {
    "title" : {"type" : "string"},
    "startDate": {"type" : "string", 
                  "format":"date"},
    "endDate": {"type" : "string", 
                  "format":"date"},
    "dmpSearchable": {"type" : "string",
                      "enum":["yes", "no"]},
    "funding": {
      "description": "The Funding for the DMP contains funding Funding Number and what is tat number associated with for example Grant Number etc.",
      "type":"object",
      "properties" : {
        
        "grant_source": {"type" : "string",
                         "enum":["Operating Unit", "Division Project Tracking Number", "Grant Number", "Contract Number"]
                        },
        "grant_id": {"type" : "string"}
      }
    },
    "projectDescription": {"type" : "string"},
    "organizations":{
      "type": "array",
      "items": {"$ref": "#/$defs/organization"},
    },
    "primary_NIST_contact": {"$ref": "#/$defs/person"},
    "contributors":{
      "type": "array",
      "items": {"$ref": "#/$defs/contributors"},
    },
    "keyWords":{"type": "array",
                "items":{"type" : "string"}},
    "dataSize":  {"type" : "string",
                  "pattern":"^[0-9]+$"},
    "sizeUnit": {"type" : "string",
                  "enum":["MG", "GB", "TB"]},
    "softwareDevelopment":{
      "type":"object",
      "properties" : {
        "development": {"type" : "string",
                        "enum":["yes", "no"]},
        "softwareUse": {"type" : "string",
                        "enum":["internal", "external", "both"]},
        "softwareDatabase": {"type" : "string",
                        "enum":["yes", "no"]},
        "softwareWebsite": {"type" : "string",
                        "enum":["yes", "no"]},
      }
    },
    "technicalResources":{"type": "array",
                          "items":{"type" : "string"}},
    "ethical_issues": {
      "type":"object",
      "properties" : {
        "ethical_issues_exist": {"type" : "string",
                                "enum":["yes", "no"]},
        "ethical_issues_description": {"type" : "string"},
        "ethical_issues_report": {"type" : "string"},
        "dmp_PII": {"type" : "string",
                    "enum":["yes", "no"]}
      }
    },
    "dataDescription": {"type" : "string"},
    "dataCategories": {"type": "array",
                        "items":{"type" : "string",
                                 "pattern":"^Derived$|^Working$|^Publishable$|^Published Results and SRD$"},
                        
    },
  },
  "required":["title"],
  #========================================================
  "$defs":{
    "organization":{
      "type":"object",
      "properties" : {
        "ORG_ID" : {"type" : "number"},
        "name": {"type" : "string"},
      }
    },
    "person":{
      "type":"object",
      "properties" : {
        "firstName" : {"type" : "string"},
        "lastName": {"type" : "string"},
        "orcid": {"type" : "string",
                  "pattern":"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$"},
      }
    },
    "contributors": {
      "type":"object",
      "properties" : {
        "contributor": {"$ref": "#/$defs/person"},
        "e_mail": {"type" : "string",
                   "format": "email"},
        "instituion": {"type" : "string"},
        #TO DO: add list of possible roles perhaps?
        "role": {"type" : "string"},
      }
    },
    "yes-no":{
      "type":"object",
      "properties" : {
        "val":{"type" : "string",
              "enum":["yes", "no"]},
      }
    }
  },
}

instance_filename = 'test-record.json'
    
with open(instance_filename) as instance_file:
  document = json.load(instance_file)

try:
  validate(instance=document, schema=dmp_schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
  print("Valid")
except exceptions.ValidationError as e:
  print("Validation failed!")
  print (f"Error message: {e.message}")