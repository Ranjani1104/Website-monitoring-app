from flask import Flask
from config import Config
from models import db
from routes import main
from scheduler import check_websites
from apscheduler.schedulers.background import BackgroundScheduler

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Register routes
app.register_blueprint(main)

# Scheduler (runs every 5 seconds)
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: check_websites(app), 'interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
