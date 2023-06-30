from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from spacy.tokens import Doc
import sqlite3
import spacy
import re
from src.AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from src.spacy_methods import sentence_generator, verb_matcher, get_specific_entities, verb_in_sentence
from src.db_interaction import hash_string
import os
import sys

# Get the current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the directory to the Python path
sys.path.append(current_dir)

# Flask app setup
app_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(app_dir, "db"), exist_ok=True)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app_dir, "db", "NLPdatabase.db")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Article_Reference's columns and properties here
class Article(db.Model):
    __tablename__ = 'ARTICLES_REFERENCE'
    id = db.Column(db.Integer, primary_key=True)
    art_id_hash = db.Column(db.Text)
    art_headline = db.Column(db.Text)
    sentence_id = db.Column(db.Integer)
    sentence_contents = db.Column(db.Text)
    authors = db.Column(db.Text)
    source_url = db.Column(db.Text)
    published_time = db.Column(db.Text)
    modified_time = db.Column(db.Text)
    search_id = db.Column(db.Integer)

    def __init__(self, art_id_hash, 
                 art_headline, sentence_id, 
                 sentence_contents, authors, 
                 source_url, published_time, 
                 modified_time, search_id):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.sentence_id = sentence_id
        self.sentence_contents = sentence_contents
        self.authors = authors
        self.source_url = source_url
        self.published_time = published_time
        self.modified_time = modified_time
        self.search_id = search_id

    def __repr__(self):
        return '<Article %r>' % self.sentence_contents

# Define Verbs_Reference's columns and properties here
class Verb(db.Model):
    __tablename__ = 'VERBS_REFERENCE'
    id = db.Column(db.Integer, primary_key=True)
    art_id_hash = db.Column(db.Text, db.ForeignKey('ARTICLES_REFERENCE.art_id_hash'))
    art_headline = db.Column(db.Text)
    verb_text = db.Column(db.Text)
    lemmatized_text = db.Column(db.Text)
    article_word_index = db.Column(db.Integer)
    sentence_id = db.Column(db.Integer)
    sent_word_index = db.Column(db.Integer)
    timestamp = db.Column(db.Text)
    modified_time = db.Column(db.Text)
    search_id = db.Column(db.Integer, nullable=True)

    def __init__(self, art_id_hash, 
                 art_headline, verb_text, 
                 lemmatized_text, article_word_index, 
                 sentence_id, sent_word_index, 
                 timestamp, modified_time, search_id):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.verb_text = verb_text
        self.lemmatized_text = lemmatized_text
        self.article_word_index = article_word_index
        self.sentence_id = sentence_id
        self.sent_word_index = sent_word_index
        self.timestamp = timestamp
        self.modified_time = modified_time
        self.search_id = search_id

    def __repr__(self):
        return '<Verb %r>' % self.id

# Define Entities_Reference's columns and properties here
class Entity(db.Model):
    __tablename__ = 'ENTITIES_REFERENCE'
    id = db.Column(db.Integer, primary_key=True)
    art_id_hash = db.Column(db.Text, db.ForeignKey('ARTICLES_REFERENCE.art_id_hash'))
    art_headline = db.Column(db.Text)
    entity_text = db.Column(db.Text)
    entity_type = db.Column(db.Text)
    word_index_start = db.Column(db.Integer)
    word_index_end = db.Column(db.Integer)
    sentence_id = db.Column(db.Integer)
    timestamp = db.Column(db.Text)
    modified_time = db.Column(db.Text)
    search_id = db.Column(db.Integer, nullable=True)

    def __init__(self, art_id_hash, 
                 art_headline, entity_text, 
                 entity_type, word_index_start, 
                 word_index_end, sentence_id, 
                 timestamp, modified_time, search_id):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.entity_text = entity_text
        self.entity_type = entity_type
        self.word_index_start = word_index_start
        self.word_index_end = word_index_end
        self.sentence_id = sentence_id
        self.timestamp = timestamp
        self.modified_time = modified_time
        self.search_id = search_id

    def __repr__(self):
        return '<Entity %r>' % self.search_id

# Will enter web searches to database. Quasi-foreign keys to other tables by placing this table's ID in Verb's, Entity's and Articles' tables
class Search(db.Model):
    __tablename__ = 'SEARCHES_REFERENCE'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    title = db.Column(db.String(250), default="Untitled")
    search_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    searched = db.Column(db.Boolean, default=False)
    analyzed = db.Column(db.Boolean, default=False)

    def __init__(self, url, title, search_datetime, searched, analyzed):
        self.url = url
        self.title = title
        self.search_datetime = search_datetime
        self.searched = searched
        self.analyzed = analyzed

    def __repr__(self):
        return('<Search %r>' % self.id)

# A class to provide a summary of an article, as well as generate topics, after submitting it to machine learning models
class Summary(db.Model):
    __tablename__ = 'ML_ARTICLE_SUMMARIES'
    id = db.Column(db.Integer, primary_key=True)
    art_id_hash = db.Column(db.Text, db.ForeignKey('ARTICLES_REFERENCE.art_id_hash'))
    art_headline = db.Column(db.Text)
    main_summary = db.Column(db.Text)
    sent_1_topic_1 = db.Column(db.Text)
    sent_1_topic_2 = db.Column(db.Text)
    sent_1_topic_3 = db.Column(db.Text)
    sent_2_topic_1 = db.Column(db.Text)
    sent_2_topic_2 = db.Column(db.Text)
    sent_2_topic_3 = db.Column(db.Text)
    sent_3_topic_1 = db.Column(db.Text)
    sent_3_topic_2 = db.Column(db.Text)
    sent_3_topic_3 = db.Column(db.Text)
    sent_4_topic_1 = db.Column(db.Text)
    sent_4_topic_2 = db.Column(db.Text)
    sent_4_topic_3 = db.Column(db.Text)
    sent_5_topic_1 = db.Column(db.Text)
    sent_5_topic_2 = db.Column(db.Text)
    sent_5_topic_3 = db.Column(db.Text)
    sent_6_topic_1 = db.Column(db.Text)
    sent_6_topic_2 = db.Column(db.Text)
    sent_6_topic_3 = db.Column(db.Text)
    sent_1_who = db.Column(db.Text)
    sent_2_who = db.Column(db.Text)
    sent_3_who = db.Column(db.Text)
    sent_4_who = db.Column(db.Text)
    sent_5_who = db.Column(db.Text)
    sent_6_who = db.Column(db.Text)
    sent_1_where = db.Column(db.Text)
    sent_2_where = db.Column(db.Text)
    sent_3_where = db.Column(db.Text)
    sent_4_where = db.Column(db.Text)
    sent_5_where = db.Column(db.Text)
    sent_6_where = db.Column(db.Text)
    sent_1_when = db.Column(db.Text)
    sent_2_when = db.Column(db.Text)
    sent_3_when = db.Column(db.Text)
    sent_4_when = db.Column(db.Text)
    sent_5_when = db.Column(db.Text)
    sent_6_when = db.Column(db.Text)
    summary_datetime = db.Column(db.DateTime, default=datetime.utcnow)

def __init__(
    self, art_id_hash, art_headline, main_summary,
    sent_1_topic_1, sent_1_topic_2, sent_1_topic_3,
    sent_2_topic_1, sent_2_topic_2, sent_2_topic_3,
    sent_3_topic_1, sent_3_topic_2, sent_3_topic_3,
    sent_4_topic_1, sent_4_topic_2, sent_4_topic_3,
    sent_5_topic_1, sent_5_topic_2, sent_5_topic_3,
    sent_6_topic_1, sent_6_topic_2, sent_6_topic_3,
    sent_1_who, sent_2_who, sent_3_who,
    sent_4_who, sent_5_who, sent_6_who,
    sent_1_where, sent_2_where, sent_3_where,
    sent_4_where, sent_5_where, sent_6_where,
    sent_1_when, sent_2_when, sent_3_when,
    sent_4_when, sent_5_when, sent_6_when
):
    self.art_id_hash = art_id_hash
    self.art_headline = art_headline
    self.main_summary = main_summary
    self.sent_1_topic_1 = sent_1_topic_1
    self.sent_1_topic_2 = sent_1_topic_2
    self.sent_1_topic_3 = sent_1_topic_3
    self.sent_2_topic_1 = sent_2_topic_1
    self.sent_2_topic_2 = sent_2_topic_2
    self.sent_2_topic_3 = sent_2_topic_3
    self.sent_3_topic_1 = sent_3_topic_1
    self.sent_3_topic_2 = sent_3_topic_2
    self.sent_3_topic_3 = sent_3_topic_3
    self.sent_4_topic_1 = sent_4_topic_1
    self.sent_4_topic_2 = sent_4_topic_2
    self.sent_4_topic_3 = sent_4_topic_3
    self.sent_5_topic_1 = sent_5_topic_1
    self.sent_5_topic_2 = sent_5_topic_2
    self.sent_5_topic_3 = sent_5_topic_3
    self.sent_6_topic_1 = sent_6_topic_1
    self.sent_6_topic_2 = sent_6_topic_2
    self.sent_6_topic_3 = sent_6_topic_3
    self.sent_1_who = sent_1_who
    self.sent_2_who = sent_2_who
    self.sent_3_who = sent_3_who
    self.sent_4_who = sent_4_who
    self.sent_5_who = sent_5_who
    self.sent_6_who = sent_6_who
    self.sent_1_where = sent_1_where
    self.sent_2_where = sent_2_where
    self.sent_3_where = sent_3_where
    self.sent_4_where = sent_4_where
    self.sent_5_where = sent_5_where
    self.sent_6_where = sent_6_where
    self.sent_1_when = sent_1_when
    self.sent_2_when = sent_2_when
    self.sent_3_when = sent_3_when
    self.sent_4_when = sent_4_when
    self.sent_5_when = sent_5_when
    self.sent_6_when = sent_6_when

    def __repr__(self):
        return('<Summary %r>' % self.id)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        search_content = request.form['NewsURL']
        
        # REGEX search for APNews articles'
        pattern = r'.*APNews.*'
        if re.match(pattern, search_content, re.IGNORECASE):
            
            # Populate Search item
            new_task = Search(url=search_content, search_datetime=datetime.now())
            article_dict = ap_article_dict_builder(search_content)
            new_title = article_dict["headline"]
            is_searched = True
            new_task.title = new_title
            new_task.searched = is_searched
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        else:
            flash("Invalid string. Only URLs with 'APNews' will be analyzed.")
            return redirect('/')
    else:
        searches = Search.query.all()
        return render_template('index.html', searches=searches)

# Remove all database items tied to this unique ID. 
@app.route('/delete/<int:id>')
def search_delete(id):
    search_to_delete = Search.query.get_or_404(id)
    try:
        # Delete the associate article (sentences)
        Article.query.filter_by(search_id=id).delete()

        # Delete the associated entities
        Entity.query.filter_by(search_id=id).delete()

        # Delete the associated verbs
        Verb.query.filter_by(search_id=id).delete()

        db.session.delete(search_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting this search.'

# Unique webpage of Sentences tied to unique ID
@app.route('/article/sentences/<int:id>')
def view_all_articles(id):
    articles = Article.query.filter_by(search_id=id).all()
    return render_template('sentences.html', articles=articles)

# Unique webpage of Entities tied to unique ID
@app.route('/article/entities/<int:id>')
def view_all_entities(id):
    entities = Entity.query.filter_by(search_id=id).all()
    return render_template('entities.html', entities=entities)

# Unique webpage of Verbs tied to unique ID
@app.route('/article/verbs/<int:id>')
def view_all_verbs(id):
    verbs = Verb.query.filter_by(search_id=id).all()
    return render_template('verbs.html', verbs=verbs)

# To analyze the contents of an article's URL, store them to DBs
@app.route('/article/<int:id>', methods=["GET", "POST"])
def article_search(id):
    article_to_search = Search.query.get_or_404(id)
    try:
        url = article_to_search.url
        analyzed = article_to_search.analyzed
        print(analyzed)
        if url is not None:
            if analyzed == False:
                article_dict = ap_article_dict_builder(url)
                article_txt = ap_article_full_txt(url)

                nlp = spacy.load("en_core_web_md")

                # Assign parameters to be placed into DB
                art_headline = article_dict["headline"]
                art_id_hash = hash_string(art_headline)
                list_author = article_dict["author(s)"]
                art_author = ",".join(list_author)
                source_url = article_dict["self_URL"]
                published_time = article_dict["published_time"] 
                modified_time = article_dict["modified_time"]

                # Initialize the Doc object, generate sentences, verbs, entities, from the article
                doc = nlp(article_txt)

                # Sentences
                sentences = sentence_generator(doc)
                
                # Raw Entities
                entities = get_specific_entities(sentences)
                raw_entity_list = list(entities)
                
                # Verbs
                verbs = verb_matcher(doc)
                the_verbs = verb_in_sentence(verbs, sentences, doc)

                # Populate with Article objects to add to DB
                for i, sent in enumerate(sentences):
                    sentenceClass = Article(art_headline = art_headline,
                            art_id_hash = art_id_hash,
                            sentence_id = i,
                            sentence_contents=sent,
                            authors = art_author,
                            source_url = source_url,
                            published_time = published_time,
                            modified_time = modified_time,
                            search_id = id )
                    db.session.add(sentenceClass)

                # Populate with Entity objects to add to DB
                for i, entity in enumerate(raw_entity_list):
                    entityClass = Entity(art_id_hash=art_id_hash,
                                        art_headline=art_headline,
                                        entity_text=entity[0],
                                        entity_type=entity[1],
                                        word_index_start=entity[2],
                                        word_index_end=entity[3],
                                        sentence_id = i,
                                        timestamp=datetime.now(),
                                        modified_time=modified_time,
                                        search_id = id)
                    db.session.add(entityClass)

                # Populate with Verb objects to add to DB
                for i, verb in enumerate(the_verbs):
                    verbClass = Verb(art_id_hash=art_id_hash,
                                        art_headline=art_headline,
                                        verb_text = verb[0],
                                        lemmatized_text = verb[1],
                                        article_word_index = verb[2],
                                        sentence_id = verb[4],
                                        sent_word_index = verb[5],
                                        timestamp=datetime.now(),
                                        modified_time=modified_time,
                                        search_id = id )
                    db.session.add(verbClass)

                # Search db associates this Search as being analyzed
                is_analyzed = True
                article_to_search.analyzed = is_analyzed

                # Database has grabbed Search, Verb, Entity, and Article, and commits
                db.session.add(article_to_search)
                db.session.commit()

            elif analyzed == True:
                print("already analyzed")
            else:
                article_to_search.analyzed = False
                db.session.add(article_to_search)
                db.session.commit()
                return redirect('/')        
    except:
        pass

    return redirect(f'/article/sentences/{id}')

with app.app_context():
    db.metadata.create_all(bind=db.engine, tables=[Article.__table__, Entity.__table__, Verb.__table__, Search.__table__, Summary.__table__])
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)