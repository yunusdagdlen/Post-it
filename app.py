#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

from application import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
