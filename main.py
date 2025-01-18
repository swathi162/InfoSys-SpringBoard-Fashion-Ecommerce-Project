from app import create_app, db, models
from flask_debugtoolbar import DebugToolbarExtension

app = create_app()
app.debug = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
toolbar = DebugToolbarExtension(app)

if __name__ == '__main__':
    app.run(debug=True)
