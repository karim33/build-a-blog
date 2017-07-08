from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Build-a-blog:cool@localhost:8889/Build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))


    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        error_title=""
        error_content=""
        blog_title = request.form['title']
        blog_content = request.form['content']
        if len(blog_title) >= 120 or len(blog_title)==0:
            error_title = "Limit message under 120 characthers"
            blog_title="" #displays empty title instead of the the error content
        if len(blog_content) >=1000 or len(blog_content)==0:
            error_content = "Limit message under 1000 characthers"
            blog_content=""
        if len(error_title)>0 or len(error_content)>0:
            return render_template('index.html',page_name="Build a Blog!", title=blog_title, content= blog_content, error_title=error_title, error_content=error_content)
        else:
            new_task = Blog(blog_title, blog_content)
            db.session.add(new_task)
            db.session.commit()
            return redirect("/mainpage?id="+str(new_task.id))

    posts = Blog.query.all()
    return render_template('index.html',page_name="Add a Blog Entry", posts=posts)


@app.route('/mainpage', methods=['GET'])
def add():
    blog_id = request.args.get('id')
    if blog_id==None:
        posts = Blog.query.all()
        return render_template('mainpage.html', page_name="Build A Blog", posts=posts)
    else:
        singl_post= Blog.query.filter_by(id=blog_id).first()
        return render_template('singleblog.html', post=singl_post)


if __name__ == '__main__':
    app.run()
