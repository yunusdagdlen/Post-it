## postıt project
from flask import render_template, abort, make_response

from application.controller import mod_pages
from application.models import Postit


@mod_pages.get('/postit/<uuid>')
def get_single_note(uuid):
    postit_rec = Postit.query.filter(Postit.uuid == uuid
                                     #Postit.active == True
                                     ).first()
    if postit_rec:
        return render_template('single_note.html',
                               postit=postit_rec)
    else:
        abort(make_response("Not Found", 404))

