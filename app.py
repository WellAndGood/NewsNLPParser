from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NLPdatabase.db'
db = SQLAlchemy(app)

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
    url = db.Column(db.String(200))
    search_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return('<Search %r>' % self.id)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        search_content = request.form['NewsURL']
        new_task = Search(url=search_content, search_datetime=datetime.now())
        #try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
        #except:
        #    return 'There was an issue adding your search to our records.'
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

with app.app_context():
    db.metadata.create_all(bind=db.engine, tables=[Article.__table__, Entity.__table__, Verb.__table__])
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)