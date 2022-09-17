## postıt project
from flask import render_template, abort, make_response

from application.controller import mod_pages
from application.models import Postit
from application.utils.notes_utils import SingleNoteUtils


@mod_pages.get('/postit/<uuid>')
def get_single_note(uuid):
    postit_rec=SingleNoteUtils.get_single_note(uuid)

    if postit_rec:
        return render_template('single_note.html',
                               postit=postit_rec)
    else:
        abort(make_response("Not Found", 404))

