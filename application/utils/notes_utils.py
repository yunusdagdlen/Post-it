from application import db
from application.models import Postit
from application.models import WorkSpaces


class SingleNoteUtils:
    @staticmethod
    def get_single_note(uuid):

        postit_rec = Postit.query.filter(Postit.uuid == uuid
                                         # Postit.active == True
                                         ).first()
        return postit_rec
