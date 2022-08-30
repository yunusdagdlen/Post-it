import uuid

from flask import render_template, request, redirect, url_for

from application import db
from application.controller import mod_pages
from application.models import Postit, Users
from application.workspace_utils import WorkspaceUtils


@mod_pages.route('/')
def index():
    users = Users.query.all()
    postits = Postit.query.all()
    return render_template('index.html',
                           postit_list=postits,
                           users=users)


@mod_pages.route('/add', methods=['POST', 'GET'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')

        if title or note:
            WorkspaceUtils.add_note(title, note)

            return redirect((url_for('index')))

        return redirect((url_for('index')))
    else:
        return redirect(url_for('index'))


@mod_pages.route("/del/<string:id>", methods=['POST', 'GET'])
def delete_note(id):
    if request.method == 'POST':
        note_delete_list = Postit.query.filter_by(id=id).first()
        db.session.delete(note_delete_list)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@mod_pages.route('/share/<string:id>', methods=['POST', 'GET'])
def share_note(id):
    sharing_note = Postit.query.filter_by(id=id).first()
    share_id = 'sharing-note/' + sharing_note.uuid
    return redirect(share_id, url_for('index'))


@mod_pages.route('/edit/<string:id>', methods=['POST', 'GET'])
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


@mod_pages.route('/back', methods=['POST', 'GET'])
def back():
    if request.method == 'Post':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))