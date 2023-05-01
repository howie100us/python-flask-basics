
from datetime import datetime
from flask import Flask,request,render_template, session,g
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# app configuration in flask
app.config.update(
  SECRET_KEY = "freedom#1763" , 
  SQLALCHEMY_DATABASE_URI ="postgresql://postgres:cititech@localhost/catalog_db",
  SQLALCHEMY_TRACK_MODIFICATION = False
)
# instance of the database
db = SQLAlchemy(app)

app.app_context().push()

@app.before_request
def beforeReq():
    g.string = "<br> Run before any request"


@app.route("/")
def hello():
    return "Flask demo"+g.string


@app.route("/new/")
def queryString(greetings="hello"): # greetings is default value is used if no value is passed by the user
    query_val = request.args.get("greetings",greetings) #query string
    
    return "<h1> The greetings is {0}<h1>".format(query_val)

@app.route("/user/")
@app.route("/user/<name>")
def no_queryString(name="Hugh"): # query param
    
    return "<h1> Hello there !{0}<h1>".format(name)

@app.route("/text/<string:name>")
def getName(name):
    return "<h1> Welcome :{}<h1".format(name)

@app.route("/numbers/<int:number>")
def getAge(number):
    return "<h1> Your Age :{}<h1".format(str(number))

@app.route("/add/<int:num1>/<int:num2>")
def getAgeNum(num1,num2):
    result = num1+num2
    return "<h1> the sum of :{} + {} is -> {}<h1".format(num1,num2,result) #format convert number to string


@app.route("/product/<float:num1>/<float:num2>")
def getFloat(num1,num2):
    return "<h1> the Product of:{} * {} is -> {}<h1".format(num1,num2,num1*num2)

@app.route("/home")
def homePage():
    return render_template("welcome.html")

@app.route("/movie")
def moviePage():
    moviesList =["John Wick","Black Panher","Man On Fire","iRobot","Equalizer II"]
    return render_template("movies.html",movies = moviesList,name = "Hugh")


@app.route("/tables")
def tableMoviePage():
    movieDict ={"John Wick":3.20,"Black Panher":3.50,"Man On Fire":1.57,"iRobot":2.10,"Equalizer II":1.47}
    return render_template("table_data.html",movies = movieDict,name = "Hugh")


@app.route("/filter")
def tableMoviefilterPage():
    movieDict ={"Something From Tiffany's":1.27,"John Wick":3.20,"Black Panher":3.50,"Man On Fire":1.57,"iRobot":2.10,"Equalizer II":1.47}
    return render_template("filter_data.html",movies = movieDict,name = "Hugh",film ="Christmas carrol")

@app.route("/macro")
def macroPage():
    movieDict ={"Something From Tiffany's":1.27,"John Wick":3.20,"Black Panher":3.50,"Man On Fire":1.57,"iRobot":2.10,"Equalizer II":1.47}
    return render_template("using_macro.html",movies = movieDict)

@app.route("/session")
def session_data():
    if "name" not in session:
        session["name"] = "Hugh"
        return render_template("session.html",session = session,name = session["name"])


class Publication(db.Model):
    
     id = db.Column(db.Integer, primary_key = True) 
     name = db.Column(db.String(100),nullable = False)
    
     def __init__(self,name):
         self.name = name
    
     def __repr__(self): #return string representation of the item
       return "Publisher Name : {} ".format(self.name)

     def insertPublication(punName):
       # id=idNum,name=punName to avoid init error
        pub = Publication(name=punName) # instance of table
        #// use instance of DB ti add
        db.session.add(pub)
        db.session.commit()
        
     def updatePublisherName(id):
         pub = Publication.query(id)
         pub.name = input("Please enter new Publisher name \n")   
         db.session.commit()   
        
        
        
class Book(db.Model):
     
     id = db.Column(db.Integer, primary_key = True) 
     title = db.Column(db.String(500), nullable =False, index=True)   
     author = db.Column(db.String(350))
     avg_rating = db.Column(db.Float)
     format = db.Column(db.String(50))
     image_path = db.Column(db.String(110),unique=True)
     num_pages = db.Column(db.Integer)
     pub_date = db.Column(db.DateTime, default= datetime.utcnow()) 
     #relationship
     pub_id = db.Column(db.Integer, db.ForeignKey("publication.id"))
     
     def __init__(self,title,author,avg_rating,format,image_path,num_pages,pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image_path = image_path
        self.num_pages = num_pages
        self.pub_id = pub_id
        
     def __repr__(self): #return string representation of the item
           return "TITLE : {}, By : {} ".format(self.title,self.author)    
        
     def insertBooks(btitle,bauthor,bavg_ratings,bformat,bimage_path,bnum_pages,bpub_id):
       # id=idNum,name=punName to avoid init error
        bk = Book(title=btitle,author =bauthor,avg_rating=bavg_ratings,format = bformat,
                  image_path=bimage_path,num_pages=bnum_pages,pub_id=bpub_id)
        #// use instance of DB ti add
        db.session.add(bk)
        db.session.commit() 
        
     def getAllBooks():
        books = Book.query.all() 
        return books

     def getFirstBook():# firt record in th table
      book = Book.query.first() 
      return book

     def getAllBooksType():
            return Book.query.filter_by(format="Paperback" ).all()  
     def getAllBooksByTitle():
            return Book.query.filter_by(format="Paperback" ).order_by(Book.title).all()
     
     def updateBookName(id=0):
         id = int(input("Please Enter book ID \n"))
         bookId = Book.query(id)
         bookId.title = input("Please enter new Book name \n")   
         db.session.commit()  
         
     def deleteBook(id=0): #silgle row delete
         id = int(input("Please Enter book ID \n"))
         bookId = Book.query(id)
         db.session.delete(bookId)  
         db.session.commit() 
         
     def deleteAllByIdBook(id=0): # multi row delete: if there is a foreign ker constraint, the record would hve to be deleter first in the other table
         id = int(input("Please Enter book ID \n"))
         Book.query.filter_by(pub_id =id).delete() 
         db.session.commit()                  
    


if __name__ == "__main__":
    db.create_all()#create the table if it does not exists
    
    ''' insert = input("Do you want to insert a Publisher ? Y for yes - N for no\n")
    while insert.upper() == "Y":
        name = input("Please enter Publisher Information\n")
        insertPublication(name)
        insert = input("Do you want to insert a Publisher ? Y for yes - N for no\n")
    
    insert = input("Do you want to insert a Book ? Y for yes - N for no\n")
    while insert.upper() == "Y":
        title = input("Please enter a book title\n")
        author = input("Please enter Author Name \n")
        avg_ratings = float(input("Please enter Book ratings \n"))
        format = input("Please enter Format \n")
        image = input("Please enter image path \n")
        num_page = input("Please enter number of pages \n")
        pub_id = input("Please enter Publisher ID \n")
           
        insertBooks(title,author,avg_ratings,format,image,num_page,pub_id)
        insert = input("Do you want to insert a Book ? Y for yes - N for no\n") '''
    #print(getFirstBooks(),"\n")
    print(Book.getAllBooks(),"\n")
    print(Book.getFirstBook(),"\n")
    print(Book.getAllBooksType(),"\n")
    print(Book.getAllBooksByTitle())
    app.run(debug = True)

    
