from flask import Flask,render_template,request,flash,redirect,url_for
import pickle,os
import numpy as np
import pandas as pd

app=Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
@app.route('/NBFC')
def home():
    return render_template('NBFC.html')
    
def value_predict(array_list):
    predict_list=np.array(array_list).reshape(1,9)
    model=pickle.load(open("rf.pkl","rb")) 
    scaler=pickle.load(open("scaler.pkl","rb"))
    predict_list=scaler.transform(predict_list)
    prediction = model.predict(predict_list)[0]
    return prediction,array_list
    
    
@app.route('/result', methods = ['POST']) 
def result():
    try:
        if request.method == 'POST': 
            to_predict_list = request.form  # This lines help us to get the form values , result we get is in form of dictionary
            to_predict_list = list(to_predict_list.values()) 
            to_predict_list = list(map(float, to_predict_list))
            result =  value_predict(to_predict_list)                                  
            if int(result[0])== 1: 
                prediction ='High risk of foreclosure'
            else: 
                prediction ='Low risk of foreclosure'            
            return render_template("result.html", prediction = prediction ,parameters=result[1]) 
            # 1st prediction points to the prediction variable used in HTML code.2nd predictiot points to prediction variables that we got through thisfunction
    except:
        flash("Please check the values entered",'danger')
        return render_template('NBFC.html')
        #redirect(url_for('NBFC'))
        #flash("Please check the values entered",'danger')
        #redirect(url_for('result'))
    

if __name__=='__main__':
    app.run(debug=True)



