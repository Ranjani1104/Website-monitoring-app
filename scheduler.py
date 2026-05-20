import time
import requests
from models import db, Website, Check

def check_websites(app):
    print("Running check...")

    with app.app_context():
        websites = Website.query.all()

        for w in websites:
            try:
                start = time.time()

                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "text/html"
                }

                r = requests.get(w.url, headers=headers, timeout=5)
                latency = time.time() - start

                status_code = r.status_code

                #reason/error for up/down
                if status_code >= 500:
                    status_label = "DOWN"
                    is_up = False
                elif status_code == 403:
                    status_label = "BLOCKED"
                    is_up = False
                elif status_code >= 400:
                    status_label = "WARNING"
                    is_up = False
                else:
                    status_label = "UP"
                    is_up = True

                # Add error message if not UP
                error_msg = None

                if not is_up:
                    #print(f" 🚨 ALERT: {w.url} is DOWN | Reason: {error_msg}")
                    if status_code >= 500:
                        is_up= False
                        error_msg = "Server error (5xx)"
                    elif status_code == 403:
                        is_up = True
                        error_msg = "Access blocked (403)"
                    elif status_code >= 400:
                        is_up = False
                        error_msg = f"Client error ({status_code})"
                    else:
                        is_up= True
                        error_msg = "Unknown failure"
                    print(f" 🚨 ALERT: {w.url} is DOWN | Reason: {error_msg}")

                #this line for Save to DB
                db.session.add(Check(
                    website_id=w.id,
                    status=status_code,
                    latency=latency,
                    is_up=is_up,
                    error_message=error_msg
                ))

                print(f"{w.url} → {status_label} ({status_code})")

            except requests.exceptions.RequestException as e:
                error_msg = str(e)
                print(f"🚨 ALERT: {w.url} is DOWN | Reason: {error_msg}")
                print(f"{w.url} failed: {error_msg}")

                db.session.add(Check(
                    website_id=w.id,
                    status=0,
                    latency=0,
                    is_up=False,
                    error_message=error_msg
                ))

        db.session.commit()