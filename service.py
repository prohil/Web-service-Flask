#!flask/bin/python
from app import app, db
#from app.models import User, Post

#@app.shell_context_processor
#def make_shell_context():
#    return {'db': db, ' ':  , ' ':  }
if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=True)
