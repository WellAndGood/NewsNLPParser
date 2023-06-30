# -*- coding: utf-8 -*-
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Install required dependencies

# Import necessary classes and functions

# Load the model and tokenizer

model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# If I extend the length of the input, the answer biases later input.

# article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic. A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning. Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted. The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results. Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

# Answer: the wreck of the Titanic
# article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic."

# Answer: Titan
# article_text = "A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. "

# Answer: The Vessel
# article_text = "The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning."

# Answer: Three search vessels arrived on-scene
# article_text = "Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted."

# Answer: underwater noises in the search area
# article_text = "The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results."

article_text = "Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

question_text_1 = "What's the physical location?"

where_input_1 = {
    'question': question_text_1,
    'context': article_text
}

response_1 = nlp(where_input_1)
print(response_1)

# Process the input
inputs = tokenizer(where_input_1['question'], where_input_1['context'], return_tensors="pt")
# Feed the input to the model
outputs = model(**inputs)

# Interpret the output
start_logits = outputs.start_logits
end_logits = outputs.end_logits
start_index = torch.argmax(start_logits)
end_index = torch.argmax(end_logits) + 1
answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
provided_answer_1 = response_1["answer"]
print("Answer 1:", provided_answer_1)
