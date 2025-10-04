#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.sqlite import JSON
from application.enums import PostStatus

from application import db


class Postit(db.Model):
    __tablename__ = 'postit'
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True)
    title = db.Column(db.String)
    note = db.Column(db.Text)
    uuid = db.Column(db.String, nullable=False)
    extra_info = db.Column(JSON)
    is_deleted = db.Column(db.Boolean, default=False)
    # New fields
    status = db.Column(db.Integer, nullable=False, default=PostStatus.NEW.value, server_default='0', index=True)
    rank = db.Column(db.Integer, nullable=False, default=0, server_default='0')

    __table_args__ = (
        CheckConstraint('rank >= 0 AND rank <= 5', name='ck_postit_rank_range'),
    )


class WorkSpaces(db.Model):
    __tablename__ = 'workspace'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_ip = db.Column(db.String)
    insert_date = db.Column(db.DateTime)
    requester_whois = db.Column(JSON)
    requester_country = db.Column(db.String)
