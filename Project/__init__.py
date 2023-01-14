from flask import Flask , render_template,session,redirect,request,url_for
from flask_session import Session
import sqlite3


# connect sqlite3 database
class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db',check_same_thread=False)
        self.c = self.conn.cursor()
    
    def find_user_with_email(self, email,password):
        #dict cursor
        
        query = "SELECT * FROM User WHERE Email = ? AND Password = ?"
        try:
          
          self.conn.row_factory = sqlite3.Row
          things = self.conn.execute(query, (email,password)).fetchall()
          unpacked = [{k: item[k] for k in item.keys()} for item in things]
          return unpacked[0]
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []
        
    def get_categories(self):
        query = "SELECT * FROM Category"
        try:
          self.conn.row_factory = sqlite3.Row
          things = self.conn.execute(query).fetchall()
          unpacked = [{k: item[k] for k in item.keys()} for item in things]
          return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []
        
    def get_categories_count(self):
        query = "select Category_name,count(*) as count from Ringtones join Category C on Ringtones.Ringtone_category_id = C.Category_id GROUP BY Ringtone_category_id"
        try:
          self.conn.row_factory = sqlite3.Row
          things = self.conn.execute(query).fetchall()
          unpacked = [{k: item[k] for k in item.keys()} for item in things]
          return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []

    
    
    def add_user(self,name,email,password):
        query = "INSERT INTO User (Name,Email,Password) VALUES (?,?,?)"
        try:
          self.conn.execute(query,(name,email,password))
          self.conn.commit()
          return True
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return False
        
    def get_ringtones(self):
        query = "select * from Ringtones join Category C on Ringtones.Ringtone_category_id = C.Category_id;"
        try:
          self.conn.row_factory = sqlite3.Row
          things = self.conn.execute(query).fetchall()
          unpacked = [{k: item[k] for k in item.keys()} for item in things]
          return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []
    
    def add_to_cart(self,user_id,ringtone_id):
        query = "INSERT INTO UserBasket (User_id,Ringtone_id) VALUES (?,?)"
        print("added to cart*************",user_id,"Ringtone id",ringtone_id)
        
        try:
          self.conn.execute(query,(user_id,ringtone_id))
          self.conn.commit()
          print("added to cart")
          return True
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return False
        
    def get_cart(self,user_id):
        query = "select * from UserBasket join Ringtones R on UserBasket.Ringtone_id = R.Ringtone_id where User_id = ?"
        try:
          self.conn.row_factory = sqlite3.Row
          things = self.conn.execute(query,(user_id,)).fetchall()
          unpacked = [{k: item[k] for k in item.keys()} for item in things]
          return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []
    
    def delete_from_cart(self,user_id,ringtone_id):
      query = "DELETE FROM UserBasket WHERE User_id = ? AND Ringtone_id = ?"
      try:
        self.conn.execute(query,(user_id,ringtone_id))
        self.conn.commit()
        return True
      except Exception as e:
          print(f"Failed to execute. Query: \n with error:\n{e}")
          return False
      
    def buy_cart(self,user_id,ringtone_ids):
      for ringtone_id in ringtone_ids:
        self.delete_from_cart(user_id,ringtone_id)
        query = "INSERT INTO OwnedRingtones (Userid,Ringtoneid) VALUES (?,?)"
        try:
          self.conn.execute(query,(user_id,ringtone_id))
          self.conn.commit()
        except Exception as e:
          print(f"Failed to execute. Query: \n with error:\n{e}")
          
    def get_rintone_ids_cart(self,user_id):
      query = "select Ringtone_id from UserBasket where User_id = ?"
      try:
        self.c = self.conn.cursor()
        things = self.conn.execute(query,(user_id,)).fetchall()
        ids = [item[0] for item in things]
        return ids
      except Exception as e:
          print(f"Failed to execute. Query: \n with error:\n{e}")
          return []
      
    def get_owned_ringtones(self,user_id):
      query = "select * from OwnedRingtones join Ringtones R on R.Ringtone_id = OwnedRingtones.Ringtoneid join Category C on R.Ringtone_category_id = C.Category_id where Userid=?;"
      try:
        self.conn.row_factory = sqlite3.Row
        things = self.conn.execute(query,(user_id,)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
      except Exception as e:
          print(f"Failed to execute. Query: \n with error:\n{e}")
          return []
      
    def get_owned_ringtones_categories(self,user_id):
        query = "select Category_name,count(*) as count  from Ringtones join Category C on Ringtones.Ringtone_category_id = C.Category_id join OwnedRingtones O on Ringtones.Ringtone_id = O.Ringtoneid where o.Userid = ? GROUP BY Ringtone_category_id;"
        try:
            self.conn.row_factory = sqlite3.Row
            things = self.conn.execute(query,(user_id,)).fetchall()
            unpacked = [{k: item[k] for k in item.keys()} for item in things]
            return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: \n with error:\n{e}")
            return []


            
    


db = DataBase()
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = "FesC9cBSuxakv9yN0vBY"
    return app

# ************************** Routes **************************
alerts = [1,]
@app.route("/")
def index():
    
    tempalert = alerts
    if alerts[0]:
        alerts[0] = 0
    
    
    
    categories = db.get_categories_count()
    ringtones = db.get_ringtones()
    if session.get("user_name") is None:
        data = {
            "Name": "Sign In",
            "Email": "Sign In",   
        }
        
    else:
        data = {
            "Name": session["user_name"],
            "Email": session["user_email"], 
        }
    print(data)
    print(session)
    return render_template("index.html", data=data,categories=categories,ringtones=ringtones,alerts=tempalert)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get('email')
        
        password = request.form.get('password')
        print(email,password)
        print('---')
        data = db.find_user_with_email(email,password)
        if data:
            session["user_id"] = data["Id"]
            session["user_name"] = data["Name"]
            session["user_email"] = data["Email"]
            print(session)
            return redirect(url_for('index'))
        else:
            return render_template("signin.html", message="Invalid Email or Password")
    
    email = request.form.get("floatingInput")
    password = request.form.get("floatingPassword")
    print(email,password)
    print('***')
    return render_template("signin.html",message="Welcome")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name=request.form.get("signUpName")
        email=request.form.get("signUpEmail")
        password=request.form.get("signUpPassword")
        db.add_user(name,email,password)
        session["user_name"] = name
        session["user_email"] = email
        data = db.find_user_with_email(email,password)
        session["user_id"] = data["Id"]
        print(session)
        return redirect(url_for("index"))
    return render_template("signup.html")

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for('index'))

# add item to cart
@app.route("/add_to_cart/<id>", methods=["POST", "GET"])
def add_to_cart(id):
    global alerts
    alerts = [1,]
    if session.get("user_name") is None:
        return redirect(url_for('signin'))
    else:    
        print('----******************************* ',id)
        #  show succes message and redirect to cart page
        userid=session["user_id"]
        db.add_to_cart(userid,id)    
        return redirect(url_for('index'))
    
@app.route("/cart")
def cart():
    if session.get("user_name") is None:
        return redirect(url_for('signin'))
    
    
    
    tempalert = alerts
    if alerts[0]:
        alerts[0] = 0
    
    
    
    categories = db.get_categories_count()
    ringtones = db.get_ringtones()
    if session.get("user_name") is None:
        data = {
            "Name": "Sign In",
            "Email": "Sign In",   
        }
        return render_template("cart.html", data=data,categories=categories,ringtones=ringtones,alerts=tempalert)
        
    else:
        data = {
            "Name": session["user_name"],
            "Email": session["user_email"], 
        }
        cartdata = db.get_cart(session["user_id"])
        
    return render_template("cart.html", data=data,categories=categories,ringtones=ringtones,alerts=tempalert,cartdata=cartdata)

@app.route("/delete_from_cart/<id>", methods=["POST", "GET"])
def delete_from_cart(id):
    global alerts
    alerts = [1,]
    if session.get("user_name") is None:
        return redirect(url_for('signin'))
    else:    
        print('----******************************* ',id)
        #  show succes message and redirect to cart page
        userid=session["user_id"]
        db.delete_from_cart(userid,id)    
        return redirect(url_for('cart'))

@app.route("/buy_cart", methods=["POST", "GET"])
def buy_cart():
    global alerts
    alerts = [1,]
    if session.get("user_name") is None:
        return redirect(url_for('signin'))
    else:    
        print('----******************************* ')
        #  show succes message and redirect to cart page
        userid=session["user_id"]
        ringtone_ids = db.get_rintone_ids_cart(userid)
        db.buy_cart(userid,ringtone_ids)    
        return redirect(url_for('order_complete'))


@app.route("/ownedringtones")
def ownedringtones():
    if session.get("user_name") is None:
        return redirect(url_for('signin'))
    else:
        userid = session["user_id"]    
        print('----******************************* ')
        #  show succes message and redirect to cart page
        categories = db.get_owned_ringtones_categories(userid)
        
       
        ringtones = db.get_owned_ringtones(userid)
        
        data = {
            "Name": session["user_name"],
            "Email": session["user_email"], 
        }
            
        return render_template("owned.html", data=data,categories=categories,ringtones=ringtones,alerts=[])

@app.route("/order-complete/")
def order_complete():
    tempalert = alerts
    if alerts[0]:
        alerts[0] = 0
    
    
    
    categories = db.get_categories_count()
    ringtones = db.get_ringtones()
    if session.get("user_name") is None:
        data = {
            "Name": "Sign In",
            "Email": "Sign In",   
        }
        
    else:
        data = {
            "Name": session["user_name"],
            "Email": session["user_email"], 
        }

    return render_template("order-complete.html", data=data,categories=categories,ringtones=ringtones,alerts=tempalert)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)