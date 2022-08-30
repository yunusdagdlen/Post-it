import uuid

from application import db
from application.models import Postit


class WorkspaceUtils:
    @staticmethod
    def add_note(title, note):
        is_success = True
        unique_id = uuid.uuid4().hex
        if unique_id:
            new_note = Postit(title=title, note=note, uuid=unique_id)
            db.session.add(new_note)
            db.session.commit()
        else:
            is_success = False
        return is_success