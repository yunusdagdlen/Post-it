#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
from sqlalchemy.dialects.sqlite import JSON

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


class WorkSpaces(db.Model):
    __tablename__ = 'workspace'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_ip = db.Column(db.String)
    insert_date = db.Column(db.DateTime)
    requester_whois = db.Column(JSON)
    requester_country = db.Column(db.String)
