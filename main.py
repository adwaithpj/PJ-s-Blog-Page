from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, URL, Length, NumberRange
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
Bootstrap5(app)


class Addnewpost(FlaskForm):
    title = StringField("Blog title", validators=[DataRequired()])
    subtitle = StringField("Blog subtitle", validators=[DataRequired()])
    date = DateField("Date of Creation", default=date.today(), validators=[DataRequired()])
    author = StringField("Author's Name", validators=[DataRequired()])
    img_url = StringField("Banner Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Body')
    submit = SubmitField("Submit")


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = []
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/blog/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalars().first()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post

@app.route('/new-post', methods=['POST', 'GET'])
def add_new_post():
    form1 = Addnewpost()
    if form1.validate_on_submit():
        new_post = BlogPost(
            title=form1.title.data,
            subtitle=form1.subtitle.data,
            date=form1.date.data,
            body=form1.body.data,
            author=form1.author.data,
            img_url=form1.img_url.data

        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template('make-post.html', form=form1, post_value="New Post")


# TODO: edit_post() to change an existing blog post

@app.route('/edit-post/<int:blog_id>', methods=['GET', 'POST'])
def edit_post(blog_id):
    post = db.get_or_404(BlogPost, blog_id)
    edit_form = Addnewpost(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.body = edit_form.body.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        # db.session.execute()
        db.session.commit()
        return redirect(url_for("show_post",post_id=post.id))

    return render_template('make-post.html', form=edit_form, post_value="Edit Post"),404


# TODO: delete_post() to remove a blog post from the database

@app.route('/delete/<int:blog_id>')
def delete_post(blog_id):
        db.session.execute(db.delete(BlogPost).where(BlogPost.id == blog_id))
        db.session.commit()
        return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
