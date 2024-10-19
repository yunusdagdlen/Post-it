#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

from application.models import Postit


class SingleNoteUtils:
    @staticmethod
    def get_single_note(uuid):
        postit_rec = Postit.query.filter(Postit.uuid == uuid
                                         # Postit.active == True
                                         ).first()
        return postit_rec
