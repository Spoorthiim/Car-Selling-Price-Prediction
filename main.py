from flask  import Flask, render_template, request
import pickle
import numpy as np
import sklearn

app = Flask(__name__)
model = pickle.load(open('model_RFR.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Petrol=1
    Transmission_Manual=1
    
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Kms_Driven2=np.log(Kms_Driven)
        Year=2024-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Manual=request.form['Transmission_Mannual']
        if(Transmission_Manual=='Mannual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',pred="Sorry you cannot sell this car")
        else:
            return render_template('index.html',pred=" {} lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=0000)
    #app.run(debug=True)