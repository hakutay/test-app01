from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db" #使うDB
db = SQLAlchemy(app)

class Post(db.Model): #DBについて
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime,nullable=False)

@app.route("/",methods=["GET","POST"]) #トップページ
def index():
    if request.method == "GET": #リクエスト方法がGETのとき
        posts = Post.query.order_by(Post.due).all() #投稿を全て取ってくる
        return render_template("index.html",posts=posts,today=date.today())
    else: #リクエスト方法がPOSTのとき
        title = request.form.get("title")
        detail = request.form.get("detail")
        due = request.form.get("due")

        #文字型の日付をキャスト
        due = datetime.strptime(due,"%Y-%m-%d")
        new_post = Post(title=title,detail=detail,due=due)

        #ここでDBに保存してる
        db.session.add(new_post)
        db.session.commit()

        return redirect("/") #トップページにリダイレクト

@app.route("/create") #入力ページ
def create():
    return render_template("create.html")


@app.route("/detail/<int:id>") #詳細ページ
def read(id):
    post = Post.query.get(id) #該当するIDだけを取ってこい
    return render_template("detail.html",post=post)


@app.route("/update/<int:id>",methods=["GET","POST"]) #編集ページ
def uedate(id):
    post = Post.query.get(id) #該当するIDだけを取ってこい
    if request.method == "GET":
        return render_template("update.html",post=post)
    else:
        post.title = request.form.get("title")
        post.detail = request.form.get("detail")
        due = datetime.strptime(request.form.get("due"),"%Y-%m-%d")

        db.session.commit()
        return redirect("/")

@app.route("/delete/<int:id>") #タスク削除
def delete(id):
    post = Post.query.get(id) #該当するIDだけを取ってこい

    #ここで削除してる
    db.session.delete(post)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run()
