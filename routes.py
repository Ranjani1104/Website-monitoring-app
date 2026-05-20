from flask import Blueprint, render_template, redirect, request, current_app
from models import db, Website, Check
from scheduler import check_websites

main = Blueprint('main', __name__)

#home part
@main.route('/')
def home():
    websites = Website.query.all()
    results = []

    for w in websites:
        latest = Check.query.filter_by(website_id=w.id)\
                            .order_by(Check.id.desc())\
                            .first()

        #Uptime calculation part
        checks = Check.query.filter_by(website_id=w.id).all()

        if checks:
            total = len(checks)
            up = len([c for c in checks if c.is_up])
            uptime = round((up / total) * 100, 2)
        else:
            uptime = 0

        results.append({
            "id": w.id,
            "url": w.url,
            "status": latest.is_up if latest else None,
            "latency": latest.latency if latest else None,
            "status_code": latest.status if latest else None,
            "checked_at": latest.checked_at if latest else None,
            "uptime": uptime
        })

    return render_template('index.html', results=results)


#Adding websites part
@main.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        url = request.form.get('url')

        print("URL RECEIVED:", url)

        if not url:
            return "No URL provided"

        if not url.startswith("http"):
            url = "http://" + url

        db.session.add(Website(url=url))
        db.session.commit()

        return redirect('/')

    return render_template('add.html')

#Delete website part
@main.route('/delete/<int:id>')
def delete(id):
    website = Website.query.get(id)

    if website:
        db.session.delete(website)
        db.session.commit()

    return redirect('/')


#ready button
@main.route('/check-now')
def check_now():
    check_websites(current_app)
    return redirect('/')
