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

article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic. A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning. Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted. The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results. Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

question_text_1 = 'Who is the main subject of this article?'

# First set of questions
who_input_1 = {
    'question': question_text_1,
    'context': article_text
}

print('Quesion 1: ', question_text_1)

response_1 = nlp(who_input_1)
print(response_1)

# Process the input
inputs_1 = tokenizer(who_input_1['question'], who_input_1['context'], return_tensors="pt")
# Feed the input to the model
outputs = model(**inputs_1)

# Interpret the output
start_logits = outputs.start_logits
end_logits = outputs.end_logits
start_index = torch.argmax(start_logits)
end_index = torch.argmax(end_logits) + 1
answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_1['input_ids'][0][start_index:end_index]))
provided_answer_1 = response_1["answer"]
print("Answer 1:", provided_answer_1)


# Use the response from Question 1 to feed into Question 2
question_text_2 = f"Besides '{provided_answer_1}', who is the main character of this article?"
print("Question 2: ", question_text_2)

who_input_2 = {
    'question': question_text_2,
    'context': article_text
}

response_2 = nlp(who_input_2)
print(response_2)

# Process the input
inputs_2 = tokenizer(who_input_2['question'], who_input_2['context'], return_tensors="pt")
# Feed the input to the model
outputs_2 = model(**inputs_2)

# Interpret the output
start_logits_2 = outputs_2.start_logits
end_logits_2 = outputs_2.end_logits
start_index_2 = torch.argmax(start_logits_2)
end_index_2 = torch.argmax(end_logits_2) + 1
answer_2 = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_2['input_ids'][0][start_index_2:end_index_2]))
provided_answer_2 = response_2["answer"]
print("Answer:", provided_answer_2)


# Use the response from Question 1 and 2 to feed into Question 3

question_text_3 = f"Besides '{provided_answer_1}' and '{provided_answer_2}', who is the main character of this article?"
print("Question 3: ", question_text_3)

who_input_3 = {
    'question': question_text_3,
    'context': article_text
}

response_3 = nlp(who_input_3)
print(response_3)

# Process the input
inputs_3 = tokenizer(who_input_3['question'], who_input_3['context'], return_tensors="pt")
# Feed the input to the model
outputs_3 = model(**inputs_3)

# Interpret the output
start_logits_3 = outputs_3.start_logits
end_logits_3 = outputs_3.end_logits
start_index_3 = torch.argmax(start_logits_3)
end_index_3 = torch.argmax(end_logits_3) + 1
answer_3 = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_3['input_ids'][0][start_index_3:end_index_3]))
provided_answer_3 = response_3["answer"]
print("Answer:", provided_answer_3)


