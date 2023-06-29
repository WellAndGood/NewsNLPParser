# -*- coding: utf-8 -*-
import torch
# from haystack.pipelines import ExtractiveQAPipeline
from haystack import Pipeline, ExtractiveQAPipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

from haystack.telemetry import tutorial_running
import logging

tutorial_running(3)
logging.basicConfig(format="%(levelname)s - %(name)s - %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)



# Install required dependencies

# Import necessary classes and functions

# Load the model and tokenizer
model_name = "deepset/deberta-v3-large-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# pipeline = ExtractiveQAPipeline(model=model, tokenizer=tokenizer)

pipeline = Pipeline()
pipeline.add_node("question_answering", ExtractiveQAPipeline(model=model, tokenizer=tokenizer, inputs=["query", "documents"]))


# model = AutoModelForQuestionAnswering.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# Get predictions
# nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)



# If I extend the length of the input, the answer biases later input.

# article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic. A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning. Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted. The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results. Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

# Answer: the wreck of the Titanic
article_text = "A Canadian military surveillance aircraft detected underwater noises as a massive operation searched early Wednesday in a remote part of the North Atlantic for a submersible that vanished while taking five people down to the wreck of the Titanic."

# Answer: Titan
# article_text = "A statement from the U.S. Coast Guard did not elaborate on what rescuers believed the noises could be, though it offered a glimmer of hope for those lost aboard the Titan. "

# Answer: The Vessel
# article_text = "The vessel is estimated to have as little as a day’s worth of oxygen left if it is still functioning."

# Answer: Three search vessels arrived on-scene
# article_text = "Three search vessels arrived on-scene Wednesday morning, including one that has side-scanning sonar capabilities, the Coast Guard tweeted."

# Answer: underwater noises in the search area
# article_text = "The Coast Guard wrote on Twitter that a Canadian military surveillance aircraft had “detected underwater noises in the search area” and that an underwater robot sent to search that area has so far “yielded negative results."

# article_text = "Still, authorities pushed on Wednesday to get salvage equipment to the scene in case the sub is found."

question_text_1 = "What's the physical location?"

where_input_1 = {
    'question': question_text_1,
    'context': article_text
}

result = pipeline.run(query=question_text_1, context=article_text)

answer = result['answers'][0]['answer']
print(answer)
