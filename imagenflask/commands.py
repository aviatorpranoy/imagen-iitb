import click
from flask.cli import click_appcontext

from imagenflask import db
from imagenflask.models import User, Post

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()