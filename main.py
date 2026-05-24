from flask import Flask
from config import Config
from models import db
from routes import main
from scheduler import check_websites
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_flask_exporter import PrometheusMetrics
import os

# Create app
app = Flask(__name__)
app.config.from_object(Config)

metrics = PrometheusMetrics(app)

# Initialize DB
db.init_app(app)

# Register routes
app.register_blueprint(main)

# Create tables
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Scheduler setup
scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(lambda: check_websites(app), 'interval', seconds=5)
    scheduler.start()

# Prevent multiple scheduler runs
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    start_scheduler()

# Run app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)