from app import app, Article, Entity, Verb, Search, Summary

import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BartTokenizer, BartForConditionalGeneration

with app.app_context():
    results = Search.query.all()
    




model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Process the input
input_text  = """A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic.
A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning.
Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted.
The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results.”
Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found.
"""
# inputs = tokenizer(text, return_tensors="pt")
inputs = tokenizer.encode(input_text, return_tensors="pt")

# Feed the input to the model
# outputs = model(**inputs))
output = model.generate(inputs, max_new_tokens=150)
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print(decoded_output)


# Interpret the output
# predicted_class = torch.argmax(outputs.logits, dim=1).item()
# predicted_class = outputs.logits

# Use the model's output for further processing
# print("Predicted class:", predicted_class)