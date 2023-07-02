import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..app import app, Article, Entity, Verb, Search, Summary

import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BartTokenizer, BartForConditionalGeneration


with app.app_context():
    results = Search.query.all()

print(results)


