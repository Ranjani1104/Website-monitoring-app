import time, requests
from models import db, Website, Check

def check_websites(app):
    print("Running check...")

    with app.app_context():
        websites = Website.query.all()

        for w in websites:
            try:
                start = time.time()
                r = requests.get(w.url, timeout=3)
                latency = time.time() - start

                is_up = True if r.status_code == 200 else False

                db.session.add(Check(
                    website_id=w.id,
                    status=r.status_code,
                    latency=latency,
                    is_up=is_up
                ))

            except Exception as e:
                print(f" ALERT: {w.url} is DOWN!")
                print("Error:", e)

                db.session.add(Check(
                    website_id=w.id,
                    status=0,
                    latency=0,
                    is_up=False
                ))

        db.session.commit()
