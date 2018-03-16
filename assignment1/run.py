#!/usr/bin/env python3
# coding=utf-8
from flaskr import create_app
app = create_app()

# This should be a cmd arg
is_dev = True

if __name__ == "__main__":
    if is_dev:
        app.run(port=9447, debug=True)
    else:
        app.run(port=9447, debug=False, host='0.0.0.0')
