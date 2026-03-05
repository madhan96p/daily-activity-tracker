import os
from flask import Flask, render_template, request, redirect
from models import db, Activity

app = Flask(__name__)

# Force DB to stay in root folder for visibility
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'daily_activity.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        category = request.form.get('category')
        if content:
            new_activity = Activity(content=content, category=category)
            db.session.add(new_activity)
            db.session.commit()
        return redirect('/')
    
    # Show active items first, then completed ones
    activities = Activity.query.order_by(Activity.is_completed, Activity.date_created.desc()).all()
    return render_template('index.html', activities=activities)

@app.route('/toggle/<int:id>')
def toggle(id):
    activity = Activity.query.get_or_404(id)
    activity.is_completed = not activity.is_completed
    db.session.commit()
    return redirect('/')

# Optional: Add this to delete entries
@app.route('/delete/<int:id>')
def delete(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)