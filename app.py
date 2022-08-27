from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yunus/PycharmProjects/Postit/postit.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    postits = Postit.query.all()
    return render_template('index.html',
                           postit_list=postits)


@app.route('/add', methods=['POST', 'GET'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        if title or note == len(title) < 0 or len(note) < 0:
            save_note = Postit(title=title, note=note)
            db.session.add(save_note)
            db.session.commit()
            return redirect((url_for('index')))
        else:
            pass
        return redirect((url_for('index')))

    else:
        return redirect(url_for('index'))


@app.route("/del/<string:id>", methods=['POST', 'GET'])
def delete_note(id):
    if request.method == 'POST':
        note_delete_list = Postit.query.filter_by(id=id).first()
        db.session.delete(note_delete_list)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/share/<string:id>/Postit.unique_id', methods=['POST', 'GET'])
def share_note(id):
    sharing_note = Postit.query.filter_by(id=id).first()
    return render_template('shared_notes.html',
                           note=sharing_note)


@app.route('/edit/<string:id>', methods=['POST', 'GET'])
def edit_note(id):
    edit_note = Postit.query.filter_by(id=id).first()
    title = request.form.get('title')
    note = request.form.get('note')
    db.session.delete(edit_note)
    newNote = Postit(title=title, note=note)
    db.session.add(newNote)
    db.session.commit()
    return render_template('edit_notes.html',
                           note=edit_note)


@app.route('/back', methods=['POST', 'GET'])
def back():
    if request.method == 'Post':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


class Postit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    note = db.Column(db.Text)

print(str(uuid.uuid4()))
if __name__ == '__main__':
    app.run()
