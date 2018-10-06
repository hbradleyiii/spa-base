from app import create_app
from app.models import db, User


@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}
