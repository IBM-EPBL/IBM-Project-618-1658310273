import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request
from scripts.File_Extractor import index_to_information

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Integer,String,ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import numpy as np
from keras.utils import load_img, img_to_array



current_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(current_dir,'authenticate.sqlite3')
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

model=load_model("nutrition.h5")

class Users(db.Model):
    _tablename_='users'
    user_name=db.Column(db.String,primary_key=True,nullable=False)
    password=db.Column(db.String,nullable=False)

def print_info (info_dict : dict) -> str:
    info = []
    for i in info_dict.keys():
        info.append(f"{i} : {info_dict[i]}")
    return " ".join(info)


@app.route('/', methods=["GET","POST"])
def hello_world():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        username=request.form["user_name"]
        #print(username)
        delt=Users.query.filter(Users.user_name==username)
        try:
            print(delt[0])
        except:
            print('hi')
            return render_template('error.html')
        password=request.form["password"]
        user=Users.query.all()
        delt1=Users.query.filter(Users.password==password)
        try:
            print(delt1[0])
        except:
            print('hey')
            return render_template('error.html')
        #print(user)
        return render_template('index.html',user=user)
engine=create_engine("sqlite:///./authenticate.sqlite3")

@app.route('/register', methods=["GET","POST"])

def register():
    if request.method=="GET":
        return render_template("register.html")
    elif request.method=="POST":
#username=request.form["user_name"]
        #password=request.form["password"]
        with Session(engine,autoflush=False) as session:
            session.begin()
            user=Users(user_name=request.form['user_name'],password=request.form['password'])
            session.add(user)
            session.flush()
            session.commit()
        return render_template("register.html")

@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def upload():
	if request.method=='POST':
		f=request.files['image']
		basepath=os.path.dirname(__file__)
		filepath=os.path.join(basepath,'uploads',f.filename)
		f.save(filepath)
		img=image.load_img(filepath,target_size=(32,32))
		x = img_to_array(img)
		x = np.expand_dims (x,axis = 0)
		predictions = (model.predict(x) > 0.5).astype("int32")
		print(predictions)
		index = predictions[0].nonzero()[0][0]
		predicted_class_info = index_to_information(index,[r"csv/index_list.csv",r"csv/nutrients_list.csv",r"csv/price_list.csv"] )
		text="The Fruit is : " + predicted_class_info['NAME']
	return print_info(predicted_class_info )
if __name__=='__main__':
    app.run(debug=True)