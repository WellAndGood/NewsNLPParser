# -*- coding: utf-8 -*-
import torch
from transformers import AutoModelForQuestionAnswering,  AutoTokenizer, pipeline

# Load the model and tokenizer
model_name = "deepset/minilm-uncased-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# Get predictions
# nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)



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

# article_text = "Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

# question_text_1 = "Where does this take place?"
# question_text_1 = "Where is this?"
question_text_1 = 'When does this sentence take place?'

where_input_1 = {
    'question': question_text_1,
    'context': article_text
}

response_1 = nlp(where_input_1)

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Process the input
inputs_1 = tokenizer.encode_plus(where_input_1['question'], where_input_1['context'], add_special_tokens=True, return_tensors="pt")
# Feed the input to the model
input_ids = inputs_1['input_ids'].tolist()[0]

print(input_ids)
start_scores= model(**inputs_1)["start_logits"]
end_scores = model(**inputs_1)["end_logits"]

print(start_scores, "111")
print(type(start_scores))
print(type(end_scores))
print(end_scores, "222")

# Interpret the output
answer_start = torch.argmax(start_scores)
answer_end = torch.argmax(end_scores) + 1


answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
# provided_answer_1 = response_1["answer"]
# print("Answer 1:", provided_answer_1)

if answer == '[CLS]':
    answer = "No answer found"
    start_score = 0.0
    end_score = 0.0
else:
    start_score = float(start_scores[0][answer_start].item())
    end_score = float(end_scores[0][answer_end - 1].item())

result = {
    'question': where_input_1['question'],
    'answer': answer,
    'start_score': start_score,
    'end_score': end_score
}

print(result)
