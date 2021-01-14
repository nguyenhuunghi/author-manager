from main import app as application
from api.utils.database import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(application, db)

manager = Manager(application)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # python manage.py db init
    # python manage.py db migrate
    # python manage.py db upgrade
    # python manage.py db -help
    manager.run()
