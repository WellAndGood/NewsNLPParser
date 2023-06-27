# -*- coding: utf-8 -*-
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


# Install required dependencies

# Import necessary classes and functions

# Load the model and tokenizer

model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic. A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning. Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted. The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results. Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found. The Coast Guard statement about detecting sounds underwater came after Rolling Stone reported that search teams heard “banging sounds in the area every 30 minutes. The report was encouraging to some experts because submarine crews unable to communicate with the surface are taught to bang on their submersible’s hull to be detected by sonar. “It sends a message that you’re probably using military techniques to find me and this is how I’m saying it,” said Frank Owen, a submarine search and rescue expert."

question_text = 'What is the main topic of this article?'

# First set of questions
QA_input_1 = {
    'question': question_text,
    'context': article_text
}

print('Quesion 1: ', question_text)

response_1 = nlp(QA_input_1)
print(response_1)

# Process the input
inputs = tokenizer(QA_input_1['question'], QA_input_1['context'], return_tensors="pt")
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


# Use the response from Question 1 to feed into Question 2
question_text_2 = f'What are the main topics in this article besides {provided_answer_1}?'
print("Question 2: ", question_text_2)

QA_input_2 = {
    'question': question_text_2,
    'context': article_text
}

response_2 = nlp(QA_input_2)
print(response_2)

# Process the input
inputs_2 = tokenizer(QA_input_2['question'], QA_input_2['context'], return_tensors="pt")
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

question_text_3 = f'What are the main topics in this article besides {provided_answer_1} and {provided_answer_2}?'
print("Question 3: ", question_text_3)

QA_input_3 = {
    'question': question_text_3,
    'context': article_text
}

response_3 = nlp(QA_input_3)
print(response_3)

# Process the input
inputs_3 = tokenizer(QA_input_3['question'], QA_input_3['context'], return_tensors="pt")
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




