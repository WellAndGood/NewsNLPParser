# -*- coding: utf-8 -*-
from transformers import GPT3LMHeadModel, GPT3Tokenizer
import torch


from transformers import pipeline, set_seed
generator = pipeline('text-generation', set_seed)




# Install required dependencies

# Import necessary classes and functions

# Load the model and tokenizer

model_name = "timdettmers/guanaco-65b-merged"
tokenizer = GPT3Tokenizer.from_pretrained("timdettmers/guanaco-65b-merged")
model = GPT3LMHeadModel.from_pretrained("timdettmers/guanaco-65b-merged")

# article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic. A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning. Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted. The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results. Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic."
# article_text = "A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. "
# article_text = "The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning."
# article_text = "Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted."
# article_text = "The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results."
# article_text = "Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."


question_text_1 = "What's the main location of this article?"

input_text = f"{question_text_1} - {article_text}"

input_ids = tokenizer.encode(input_text, return_tensors="pt")
output = model.generate(input_ids, max_length=100, num_return_sequences=1)

response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)


