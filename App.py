from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_BINDS'] = {'users' :'sqlite:///signup.db'  }
db = SQLAlchemy(app)

all_tasks=[

]
         

class Dolist(db.Model):
    id = db.Column( db.Integer , primary_key=True)
    task = db.Column( db.Text , nullable=False)
    date_posted = db.Column( db.DateTime , nullable=False ,default= datetime.now())
    def __repr__(self):
        return 'Task'+ str(self.id)


class SignUp(db.Model):
    __bind_key__ = 'users'
    username = db.Column( db.String(20) , primary_key=True)
    password = db.Column( db.String(20 , nullable = False))
    def __repr__(self):
        return (self.username)


@app.route("/" , methods=['GET', 'POST'])
def to():
    return(redirect("/home"))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        todo_task = request.form['task']
        new_task = Dolist(task = todo_task ) 
        db.session.add(new_task)
        db.session.commit()
        return redirect('/home')
    else:
        all_tasks = Dolist.query.order_by(Dolist.date_posted).all()
        return render_template('home.html', todo=all_tasks)


@app.route("/home/delete/<int:id>")
def delete(id):        
    delete_task=Dolist.query.get_or_404(id)
    db.session.delete(delete_task)
    db.session.commit()
    return(redirect("/home"))


@app.route('/home/update/<int:id>' , methods = ['GET','POST'])
def update(id):
    updated_task = Dolist.query.get_or_404(id)
    db.session.delete(updated_task)
    db.session.commit()
    if request.method == 'POST':
        todo_task = request.form['task']
        db.session.commit()
        return(redirect('/home'))
    else:
        return(render_template("update.html", task=updated_task))      


@app.route("/home/done/<int:id>") 
def done(id):
    done_task = Dolist.query.get_or_404(id)
    db.session.delete(done_task)
    db.session.commit()
    return(redirect("/home"))
    

@app.route("/contact")
def contact():
    return(render_template("conact.html" ))



if __name__ == "__main__":
    app.run(debug=True)
