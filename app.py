from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin, logout_user
from datetime import datetime

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'a0455de1e15d46ad995c0d40928916ef'    
db = SQLAlchemy(app)

#Create a Model of User
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<User %r>' %self.username
    
# Create a Model of Blogs
class Blog(UserMixin,db.Model):
    blog_id = db.Column(db.Integer,primary_key=True)
    tit_name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    pub_date=db.Column(db.DateTime(),nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<Blog %r>' % self.tit_name

#Create a Login Manager Object (it will hnadle login & logout functionality)
login_manager = LoginManager()
login_manager.init_app(app)

# It should take the str ID of a user, and return the corresponding user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
#Creates All Routes
@app.route('/')
def Home():
    blogss = Blog.query.all()
    return render_template('Home.html',blogs = blogss)

@app.route('/login' , methods=['GET','POST'])
def Login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter_by(username=username).first()
        if users and password == users.password:
            login_user(users)
            return redirect('/')
        else:
            flash('Invalid Credentials , Please Enter a Valid Credentials','warning')
            return redirect('/login')   
    return render_template('Login.html')

@app.route('/register', methods=['GET','POST'])
def Register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        address = request.form.get('address')
        city = request.form.get('city')
        userss = User(email=email,password=password,username=username,address=address,city=city)
        db.session.add(userss)
        db.session.commit()
        flash('Account Sucessfully Created','sucess')
        return redirect('/login')
    return render_template('Register.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/blogs',methods=['GET','POST'])
def Blogs():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('text')
        blog = Blog(tit_name=title,author=author, content=content)
        db.session.add(blog)
        db.session.commit()
        flash('Post Sucessfully Created', 'sucess')
        return redirect('/')
    return render_template('Blogs.html')

@app.route("/blogs_deatil/<int:id>")
def blogs_details(id):
    blog = Blog.query.get(id)
    return render_template('Blogs_deatails.html',blog = blog)


@app.route("/delete/<int:id>")
def del_post(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Your Post Has Been Sucessfully Deleted','sucess')
    return redirect('/')


@app.route("/edit/<int:id>", methods = ['GET','POST'])
def edit_post(id):
    blog = Blog.query.get(id)
    if request.method == 'POST':
        blog.tit_name = request.form.get('title')
        blog.author = request.form.get('author')
        blog.content = request.form.get('text')
        db.session.commit()
        flash('Your Post Has Been Sucessfully Edit', 'sucess')
        return redirect('/')
    return render_template('Edit_post.html',blog = blog)

if __name__ ==("__main__"):
  app.run(debug=True,port=5000)