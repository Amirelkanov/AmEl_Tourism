#!/usr/bin/python
# -*- coding: utf-8 -*-

from AmEl_Tourism.application import create_app

# Creating app
app = create_app()
app.app_context().push()

# Launching app
if __name__ == '__main__':
    app.run()
