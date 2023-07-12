from app import app, Article, Entity, Verb, Search, Summary
import os
from flask import Flask, render_template, url_for, request, redirect, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from src.AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from src.db_interaction import hash_string
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from flask import Blueprint



roberta_dict = {
    "what_1": "What is the main topic of this article?",
    "what_2": "What are the main topics in this article besides {provided_answer_1}?",
    "what_3": "What are the main topics in this article besides {provided_answer_1} and {provided_answer_2}?",
    "when_1": "When does this sentence take place?",
    "who_1": "Who is the main subject of this article?",
    "who_2": "Besides '{provided_answer_1}', who is the main character of this article?",
    "where_1": "When does this sentence take place?"
}

results_list = []

with app.app_context():
    searches = Search.query.all()
    results_list = searches

def search_match(url, results):

    for result in results:
        if result.url == url:
            return result

with app.app_context:
    db = SQLAlchemy(app)

APurl = "https://apnews.com/article/philadelphia-shooting-victims-8de8da4e5e3cb5d9252233372c250ba8"
result_match = search_match(APurl, results_list)
article_dict = ap_article_dict_builder(APurl)
art_headline = article_dict["headline"]
source_url = article_dict["self_URL"]
art_id_hash = hash_string(art_headline)

def first_sentences(url, low_range, upp_range):
    sentence_list = []
    with app.app_context():
        sentences = Article.query.filter_by(source_url=url).order_by(Article.sentence_id).all()
    for sent in sentences:
        sentence_list.append(sent.sentence_contents)
    return sentence_list[low_range:upp_range]

# print(result_match)

sentence_list = first_sentences(APurl, 0, 5)
print(sentence_list)


for i, sent in enumerate(sentence_list):

    response_dict = {
        "what_1": "",
        "what_2": "",
        "what_3": "",
        "when_1": "",
        "who_1": "",
        "who_2": "",
        "where_1": ""
    }

    # 'What' section

    # Roberta Base Squad - For 'what', 'when', and 'who' questions
    model_name = "deepset/roberta-base-squad2"
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    # What - Question 1
    article_text = sent
    question_text = roberta_dict["what_1"]
    QA_input = {
        'question': question_text,
        'context': article_text
    }
    response = nlp(QA_input)
    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors="pt")
    outputs = model(**inputs)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    provided_answer_1 = response["answer"]

    # What - Question 2
    question_text = roberta_dict["what_2"].format(provided_answer_1 = provided_answer_1)
    QA_input = {
        'question': question_text,
        'context': article_text
    }
    response = nlp(QA_input)
    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors="pt")
    outputs = model(**inputs)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    provided_answer_2 = response["answer"]

    # 'Who'- Question 3
    question_text = roberta_dict["what_3"].format(provided_answer_1 = provided_answer_1, provided_answer_2 = provided_answer_2)
    QA_input = {
        'question': question_text,
        'context': article_text
    }
    response = nlp(QA_input)
    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors="pt")
    outputs = model(**inputs)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    provided_answer_3 = response["answer"]

    # Update response_dict values
    response_dict["what_1"] = provided_answer_1
    if len(provided_answer_2) > 0 and provided_answer_2 != provided_answer_1:
        response_dict["what_2"] = provided_answer_2

    if len(provided_answer_3) > 0 and provided_answer_3 != provided_answer_1 and provided_answer_3 != provided_answer_2:
        response_dict["what_3"] = provided_answer_3

    # 'When' section

    question_text = roberta_dict["when_1"]
    when_input_1 = {
        'question': question_text,
        'context': sent
    }
    response = nlp(when_input_1)
    # Process the input
    inputs_1 = tokenizer(when_input_1['question'], when_input_1['context'], return_tensors="pt")
    # Feed the input to the model
    outputs = model(**inputs_1)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_1['input_ids'][0][start_index:end_index]))
    provided_answer = response["answer"]
    print("Answer 1:", provided_answer)
    response_dict["when_1"] = provided_answer
    
    # 'Who' - Question 1
    question_text = sent
    roberta_dict["who_1"]

    who_input_1 = {
        'question': question_text,
        'context': sent
    }

    response = nlp(who_input_1)
    inputs = tokenizer(who_input_1['question'], who_input_1['context'], return_tensors="pt")
    outputs = model(**inputs)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_1['input_ids'][0][start_index:end_index]))
    provided_answer_1 = response["answer"]
    response_dict["who_1"] = provided_answer_1

    # Who - Question 2
    question_text = roberta_dict["who_2"].format(provided_answer_1 = provided_answer_1)
    who_input_2 = {
        'question': question_text,
        'context': sent
    }
    response = nlp(QA_input)
    inputs = tokenizer(who_input_2['question'], who_input_2['context'], return_tensors="pt")
    outputs = model(**inputs)
    
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs_1['input_ids'][0][start_index:end_index]))
    provided_answer_1 = response["answer"]
    response_dict["who_2"] = provided_answer_1

    # 'Where' section - MINILM
    # Load the model and tokenizer
    where_model_name = "deepset/minilm-uncased-squad2"
    model = AutoModelForQuestionAnswering.from_pretrained(where_model_name)
    tokenizer = AutoTokenizer.from_pretrained(where_model_name)

    where_nlp = pipeline('question-answering', model=where_model_name, tokenizer=where_model_name)

    # Where - Question 1
    article_text = sent
    question_text = roberta_dict["where_1"]
    QA_input = {
        'question': question_text,
        'context': sent
    }
    response = nlp(QA_input)
    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors="pt")
    outputs = model(**inputs)

    # Interpret the output
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    provided_answer_1 = response["answer"]

    response_dict["where_1"] = provided_answer_1

    print(response_dict)

    summaryClass = Summary(art_id_hash=art_id_hash,
                           art_headline = art_headline,
                           sentence_id = i,
                           source_url = source_url,
                            sent_what_1 = response_dict["what_1"],
                            sent_what_2 = response_dict["what_2"],
                            sent_what_3 = response_dict["what_3"],
                            sent_who_1 = response_dict["who_1"],
                            sent_who_2 = response_dict["who_2"],
                            sent_when = response_dict["when_1"],
                            sent_where = response_dict["where_1"],
                            summary_datetime = datetime.now()
                           )
    db.session.add(summaryClass)

db.session.commit()



def db_insert(func):
    def wrapper(*args, **kwargs):
        with current_app.app_context():
            return func(*args, **kwargs)
    return wrapper
#           