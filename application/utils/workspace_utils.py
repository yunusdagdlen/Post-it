import uuid

import requests

from application import db
from application.models import Postit
from application.models import WorkSpaces


class WorkspaceUtils:
    @staticmethod
    def add_note(title, note, workspace_id):
        is_success = True
        unique_id = uuid.uuid4().hex
        if unique_id:
            new_note = Postit(title=title,
                              note=note,
                              uuid=unique_id,
                              workspace_id=workspace_id,
                              active=True)
            db.session.add(new_note)
            db.session.commit()
        else:
            is_success = False
        return is_success


    @staticmethod
    def edit_note(title,note,uuid):
        workspace_edit = Postit.query.filter_by(uuid=uuid).first()
        edited_note=note
        edited_title=title
        workspace_edit.title=edited_title
        workspace_edit.note=edited_note
        db.session.commit()
    @staticmethod
    def delete_note(id):
        is_success = True
        if id:
            note_delete = Postit.query.filter_by(id=id).first()
            db.session.delete(note_delete)
            db.session.commit()
        else:
            is_success = False
        return is_success

    @staticmethod
    def get_workspace_notes(workspace_uuid):
        is_success = True
        postits_records=[]
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid).first()
        if workspace_rec:
            postits_records = Postit.query.filter_by(workspace_id=workspace_rec.uuid).all()
        else:
            is_success = False
        return postits_records

    @staticmethod
    def create_workspace():
        unique_id = uuid.uuid4().hex
        new_workspace = WorkSpaces(uuid=unique_id)
        db.session.add(new_workspace)
        db.session.commit()
        return unique_id

