from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField
import joblib
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'y7854k_op'  # Replace 'your_secret_key' with a secret key

class CarPriceForm(FlaskForm):
    Year = IntegerField('Showroom Released Year')
    Present_Price = FloatField('Showroom Price (In lakhs)')
    Kms_Driven = IntegerField('Kilometers Driven')
    Owner = IntegerField('Number of Owners')
    Fuel_Type_Petrol = SelectField('Fuel Type', choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('CNG', 'CNG')])
    Seller_Type_Individual = SelectField('Seller Type', choices=[('Dealer', 'Dealer'), ('Individual', 'Individual')])
    Transmission_Mannual = SelectField('Transmission Type', choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])

# Load the trained model using joblib
model = joblib.load('random_forest_regression_model_1 (1).joblib')

@app.route('/')
def home():
    return render_template('index.html', form=CarPriceForm())

@app.route('/prediction', methods=['POST'])
def prediction():
    form_data = request.form
    input_data = [
        int(form_data['Year']),
        float(form_data['Present_Price']),
        int(form_data['Kms_Driven']),
        int(form_data['Owner']),
        2020 - int(form_data['Year']),
        1 if form_data['Fuel_Type_Petrol'] == 'Petrol' else 0,
        1 if form_data['Seller_Type_Individual'] == 'Individual' else 0,
        1 if form_data['Transmission_Mannual'] == 'Manual' else 0
    ]

    # Make prediction using the loaded model
    predicted_price = model.predict([input_data])[0]

    # Randomly select a car image from the list
    car_images = [
        'https://www.carscoops.com/wp-content/uploads/2023/02/Toyota-Supra-EV-23-Carscoops-1.jpg',
        'https://e1.pxfuel.com/desktop-wallpaper/1006/684/desktop-wallpaper-nissan-gtr-r35-posted-by-cute-nissan-gtr-modified.jpg',
        'https://w0.peakpx.com/wallpaper/117/419/HD-wallpaper-bmw-m4-highly-modified-bmw-cars-bmw-m4-modified-tuned-red.jpg',
        'https://c4.wallpaperflare.com/wallpaper/327/192/923/nissan-skyline-gt-r-nissan-skyline-gt-r-r34-car-vehicle-wallpaper-thumb.jpg',
        'https://www.carblogindia.com/wp-content/uploads/2021/09/Best-Maruti-Omni-Modification.jpg'
    ]
    selected_car_image = random.choice(car_images)

    # Render the result template with dynamic content
    return render_template('result.html', predicted_price=predicted_price, car_image=selected_car_image)

if __name__ == '__main__':
    app.run(debug=True)
