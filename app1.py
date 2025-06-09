from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#initialise app 5
app=Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    #home page - only ID, Prod, Model and ImgURL
    sql = """SELECT Product.ProductID, Producers.Name, Product.Model, Product.ImageURL
    FROM Product
    JOIN Producers ON Producers.ProducerID=Product.ProducerID;"""
    results = query_db(sql)
    return render_template("home.html",results=results)

@app.route("/product/<int:id>")
def product(id):
    #just one product basd on id
    sql= """SELECT * FROM Product
            JOIN Producers ON Producers.ProducerID=Product.ProducerID
            WHERE Product.ProductID=?;"""
    result = query_db(sql, (id,), True)
    return render_template("product.html", product=result)

if __name__ == "__main__":
    app.run(debug=True)