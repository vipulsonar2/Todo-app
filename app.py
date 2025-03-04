from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy       #SQLAlchemy is a orm mapper facilitiate to make changes in database through python
from datetime import datetime

# initilization of app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
app.app_context().push()

# defining schema of database using class
class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

#    __repr__ is used for what to be print when object of Todo is printed
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route("/", methods=['GET','POST']) 
def hello_world():
    if request.method=='POST':
        # print("post")
        title=(request.form['title'])
        desc=(request.form['desc'])
        todo=Todo(title=title, desc=desc)     #instance of Todo
        db.session.add(todo)
        db.session.commit()
    
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)      #allTodo is assign to allTodo to make avalable allTodo to html using jinja2
    # return "<p>Hello, World!</p>"




@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    
    


@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    

# @app.route("/show")
# def products():
#     allTodo=Todo.query.all()
#     print(allTodo)
#     return "this is product page"
    

if __name__=="__main__":
    # app.run(debug=True)           #do not use debug=true in production
     app.run() 
