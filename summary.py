from app import app, Article, Entity, Verb, Search, Summary
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

roberta_dict = {
    "what_1": "What is the main topic of this article?",
    "what_2": "What are the main topics in this article besides {provided_answer_1}?",
    "what_3": "What are the main topics in this article besides {provided_answer_1} and {provided_answer_2}?",
    "when_1": "When does this sentence take place?",
    "who_1": "Who is the main subject of this article?",
    "who_2": "Besides '{provided_answer_1}', who is the main character of this article?",
}

mililm_dict = {
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

APurl = "https://apnews.com/article/new-york-gnats-404a0e7e699a6619c29c8a43462cdcd0"
result_match = search_match(APurl, results_list)

def first_sentences(url, low_range, upp_range):
    sentence_list = []
    with app.app_context():
        sentences = Article.query.filter_by(source_url=url).order_by(Article.sentence_id).all()
    for sent in sentences:
        sentence_list.append(sent.sentence_contents)
    return sentence_list[low_range:upp_range]

# print(result_match)

sentence_list = first_sentences(APurl, 1, 5)
print(sentence_list)


