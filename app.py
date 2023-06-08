from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from spacy.tokens import Doc
import sqlite3
import spacy
import re
from AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from spacy_methods import sentence_generator, verb_matcher, get_specific_entities, entity_counter, verb_in_sentence
from db_interaction import hash_string, article_reference_table_insert, verbs_reference_table_insert, entity_reference_table_insert

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NLPdatabase.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Article(db.Model):
    # Define Article_Reference's columns and properties here
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

    def __init__(self, art_id_hash, 
                 art_headline, sentence_id, 
                 sentence_contents, authors, 
                 source_url, published_time, 
                 modified_time):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.sentence_id = sentence_id
        self.sentence_contents = sentence_contents
        self.authors = authors
        self.source_url = source_url
        self.published_time = published_time
        self.modified_time = modified_time
    
    def __repr__(self):
        return '<Article %r>' % self.id

class Verb(db.Model):
    # Define Verbs_Reference's columns and properties here
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

    def __init__(self, art_id_hash, 
                 art_headline, verb_text, 
                 lemmatized_text, article_word_index, 
                 sentence_id, sent_word_index, 
                 timestamp, modified_time):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.verb_text = verb_text
        self.lemmatized_text = lemmatized_text
        self.article_word_index = article_word_index
        self.sentence_id = sentence_id
        self.sent_word_index = sent_word_index
        self.timestamp = timestamp
        self.modified_time = modified_time

    def __repr__(self):
        return '<Verb %r>' % self.id

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

    def __init__(self, art_id_hash, 
                 art_headline, entity_text, 
                 entity_type, word_index_start, 
                 word_index_end, sentence_id, 
                 timestamp, modified_time):
        self.art_id_hash = art_id_hash
        self.art_headline = art_headline
        self.entity_text = entity_text
        self.entity_type = entity_type
        self.word_index_start = word_index_start
        self.word_index_end = word_index_end
        self.sentence_id = sentence_id
        self.timestamp = timestamp
        self.modified_time = modified_time

    def __repr__(self):
        return '<Entity %r>' % self.id

# Will enter web searches to database
class Search(db.Model):
    __tablename__ = 'SEARCHES_REFERENCE'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    title = db.Column(db.String(250), default="Untitled")
    search_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    searched = db.Column(db.Boolean, default=False)
    analyzed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return('<Search %r>' % self.id)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        search_content = request.form['NewsURL']
        pattern = r'.*APNews.*'
        if re.match(pattern, search_content, re.IGNORECASE):
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

@app.route('/delete/<int:id>')
def search_delete(id):
    search_to_delete = Search.query.get_or_404(id)
    try:
        db.session.delete(search_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting this search.'

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

                art_headline = article_dict["headline"]
                art_id_hash = hash_string(art_headline)
                list_author = article_dict["author(s)"]
                art_author = ",".join(list_author)
                source_url = article_dict["self_URL"]
                published_time = article_dict["published_time"] 
                modified_time = article_dict["modified_time"]

                # Initialize the Doc object, generate sentences, verbs, entities, from the article
                doc = nlp(article_txt)
                
                print("hello")

                # Sentences
                sentences = sentence_generator(doc)
                
                # Raw Entities
                entities = get_specific_entities(sentences)
                raw_entity_list = list(entities)
                duplicate_items = entity_counter(entities)
                
                # Verbs
                verbs = verb_matcher(doc)
                the_verbs = verb_in_sentence(verbs, sentences, doc)

                # article_reference_table_insert(sentences)
                # verbs_reference_table_insert(the_verbs)
                # entity_reference_table_insert(raw_entity_list)

                print("hello")

                for i, sent in enumerate(sentences):
                    sentenceClass = Article(art_headline = art_headline,
                            art_id_hash = art_id_hash,
                            sentence_id = i,
                            sentence_contents=sent,
                            authors = art_author,
                            source_url = source_url,
                            published_time = published_time,
                            modified_time = modified_time
                       )
                    print(sent)
                    db.session.add(sentenceClass)
                db.session.commit()

                is_analyzed = True
                # article_to_search.analyzed = is_analyzed
                db.session.add(article_to_search)
                db.session.commit()
            elif analyzed == True:
                print("already analyzed")
            else:
                article_to_search.analyzed = False
                return redirect('/')
            
    except:
        pass

    # print(is_analyzed)
    return render_template('analysis.html')

with app.app_context():
    db.metadata.create_all(bind=db.engine, tables=[Article.__table__, Entity.__table__, Verb.__table__, Search.__table__])
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)