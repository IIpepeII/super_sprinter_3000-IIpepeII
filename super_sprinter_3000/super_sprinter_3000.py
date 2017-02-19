# all the imports
import os
from flaskr.connectdatabase import ConnectDatabase
from super_sprinter_3000.models import Userstories
from flask import Flask, request, g, redirect, url_for, render_template

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    DATABASE=os.path.join(app.root_path, 'super_sprinter_3000.db')))

app.config.from_envvar('SUPER_SPRINTER_3000_SETTINGS', silent=True)

def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Userstories], safe=True)

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()

@app.route('/')
def show_entries():
    stories = Userstories.select().order_by(Userstories.id.asc())

    return render_template('list.html', stories=stories)

@app.route('/empty_story')
def empty_user_story():
    return render_template('form.html', story=None)

@app.route('/add_user_story', methods=['POST'])
def add_user_story():
    new_entry = Userstories.create(story_title=request.form['story_title'],
                                   user_story=request.form['user_story'],
                                   acceptance_criteria=request.form['acceptance_criteria'],
                                   business_value=request.form['business_value'],
                                   estimation=request.form['estimation'],
                                   status=request.form['status'])
    new_entry.save()
    return redirect('/')

@app.route('/chosen_story', methods=['POST'])
def chosen_story():
    story_id = request.form['story_id']
    chosen_story = Userstories.get(Userstories.id == story_id)
    return render_template('form.html', story=chosen_story)

@app.route('/edit_user_story', methods=['POST'])
def edit_user_story():

    story_for_update = Userstories.update(story_title=request.form['story_title'],
                                   user_story=request.form['user_story'],
                                   acceptance_criteria=request.form['acceptance_criteria'],
                                   business_value=request.form['business_value'],
                                   estimation=request.form['estimation'],
                                   status=request.form['status']).where(Userstories.id == request.form["story_id"])
    story_for_update.execute()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_user_story():

    story = Userstories.get(Userstories.id == request.form['story_id'])
    story.delete_instance()

    return redirect('/')



