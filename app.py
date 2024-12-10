from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Books(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno}: {self.title}"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        if not title or not author:
            # flash('Title and Author are required!', 'danger')
            pass
        else:
            new_book = Books(title=title, author=author)
            db.session.add(new_book)
            db.session.commit()
            # flash('Book Added Successfully!', 'success')
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 8  

    if search:
        books_query = Books.query.filter(
            (Books.title.ilike(f"%{search}%")) | (Books.author.ilike(f"%{search}%"))
        )
    else:
        books_query = Books.query

    book = books_query.paginate(page=page, per_page=per_page)
    return render_template('index.html', book=book, search=search)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        update_book = Books.query.filter_by(sno=sno).first()
        update_book.title = title
        update_book.author = author
        db.session.add(update_book)
        db.session.commit()
        return redirect('/')
    update_book = Books.query.filter_by(sno=sno).first()
    return render_template('update.html', update_book=update_book)

@app.route("/delete/<int:sno>")
def delete(sno):
    delete_book = Books.query.filter_by(sno=sno).first()
    db.session.delete(delete_book)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)