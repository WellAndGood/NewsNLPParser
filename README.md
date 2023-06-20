# Natural Language Processing Project - Associated Press Site Scraper and Text Analysis

## Overview
This application serves to demonstrate the use of text analysis libraries such as Spacy and Huggingface models to simplify the reading experience of the politically-minded.

## Background and Motivation
This solution originates from an interest to keep track of political news as they develop over time.
The Web 2.0 solution has been to use tags - often expressed along with hashtags (#) - and to group by tags when querying data; this approach is naive and has the potential for misuse and abuse. For example, someone spams popular but non-pertinent tag words to rise in the algorithms.

Instead, an AI-based approach - already used by many sites - is to extract data from the semantic contents of the article and to reference the location of these contents for future use.
This approach allows us to build a robust timeline of similar entities, and to keep track of entities over time; we can build a timeline of people and events.

## Goals
First, we look to scrape articles from the Associated Press with a single command.
Second, we extract the individual sentences; for each sentence, we save its entities - people, places, organizations - and its verbs and actions. 
Then, these results are stored, and we can later extract this data for data visualization and to feed it into machine learning models for the purpose of question answering, article summarization, and other insights. 
We also create data that we can use for labelling purposes.

## Datasets
This project uses no explicit datasets. However, the contents of the articles being fed into this solution become data for future use.

## Usage
Clone this repo
```
git clone [https://github.com/luminiphi/good-ml-project.git](https://github.com/WellAndGood/NewsNLPParser.git)
```

Create a virtual environment and activate it
```
virtualenv .env && source .env/bin/activate
```

Install all requirements
```
pip install -r requirements.txt
```

Run the web application
```
python app.py
```

## Practical Applications
The most applicable use of this solution is a current affairs digest for the political reader uninterested in partisanship; the Associated Press is rated as highly factual with minimal bias.
[Source](https://www.thefactual.com/blog/is-the-associated-press-biased/){:target="_blank"}

The secondary use is to explore alternative reading and learning methods; with the correct data visualization approach, we might stumble upon a way of displaying political information that requires fewer words, yet yields high absorption and proper recall. 

Finally, this project can be built upon to support more sophisticated methods of gathering and displaying political data. This web scraping approach might then expand to other news sites and allow for a visual comparison of tone and choice of words to describe the same events.

## Milestones
- [X] Create a working datascraper of the Associated Press
- [X] Employ the Spacy library to extract meaningful entities and actions taken by those entities
- [X] Store these results in a serverless instance of SQLite
- [X] Create a proof-of-concept application which completes all of the above using a command prompt; a URL yields database results
- [X] Use Flask/Jinja to create a CRUD application which will collect URL searches and analyze their contents, later displaying them on unique webpages.
- []
