import os
from flask import Flask, render_template, request, redirect
from models import db, Activity
from flask_migrate import Migrate

app = Flask(__name__)

# Setup SQLite Database in the local folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'daily_activity.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Create the database file if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        category = request.form.get('category')
        start_t = request.form.get('start_time')
        end_t = request.form.get('end_time')
        
        if content:
            new_activity = Activity(
                content=content, 
                category=category,
                start_time=start_t,
                end_time=end_t
            )
            db.session.add(new_activity)
            db.session.commit()
        return redirect('/')
    
    activities = Activity.query.order_by(Activity.is_completed, Activity.date_created.desc()).all()
    return render_template('index.html', activities=activities)

@app.route('/toggle/<int:id>')
def toggle(id):
    activity = Activity.query.get_or_404(id)
    activity.is_completed = not activity.is_completed
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)