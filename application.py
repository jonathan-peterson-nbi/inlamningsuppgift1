from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item_database.db' #tre slashes relativ directory
db = SQLAlchemy(app)

# initialize Item object inheriting from db.Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# when you visit it in you browser it will do GET first, when you submit the form your browser will do a POST. self submitting form needs both
@app.route('/', methods=['POST', 'GET']) 
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Item(content=item_content)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    else:
        items = Item.query.order_by(Item.date_created).all()
        return render_template('index.html', items=items)
    
@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
    app.run()