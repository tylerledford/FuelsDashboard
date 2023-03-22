import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import pdfkit
from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Read data from the CSV file
    df = pd.read_csv('fuel_data.csv')

    # Calculate the required values
    fuel_on_hand = df['fuel_on_hand'].sum()
    storage_capacity = df['storage_capacity'].sum()
    daily_demand_rate = df['daily_demand_rate'].mean()
    delivery_vehicle_health = df['delivery_vehicle_health'].mean()

    # Pass the values to the template
    return render_template('dashboard.html', fuel_on_hand=fuel_on_hand, storage_capacity=storage_capacity, 
                           daily_demand_rate=daily_demand_rate, delivery_vehicle_health=delivery_vehicle_health)


@app.route('/kyle-html')
def kyle_html():
    return render_template('kylehtml.html')

@app.route('/supply-dashboard')
def supply_dashboard():
    # Read data from the CSV file
    df = pd.read_csv('fuel_data.csv')

    # Calculate the required values
    fuel_on_hand = df['fuel_on_hand'].sum()
    storage_capacity = df['storage_capacity'].sum()
    daily_demand_rate = df['daily_demand_rate'].mean()
    delivery_vehicle_health = df['delivery_vehicle_health'].mean()

    # Pass the values to the template
    return render_template('aircraft-availability.html', fuel_on_hand=fuel_on_hand, storage_capacity=storage_capacity, 
                           daily_demand_rate=daily_demand_rate, delivery_vehicle_health=delivery_vehicle_health)

@app.route('/generate-pdf')
def generate_pdf():
    # Read data from the CSV file
    df = pd.read_csv('fuel_data.csv')

    # Generate a plot of fuel on hand
    plt.figure()
    df['fuel_on_hand'].plot(kind='bar')
    plt.xlabel('Inventory ID')
    plt.ylabel('Fuel on Hand')
    plt.title('Fuel on Hand by Inventory ID')

    # Save the plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Load the plot in the template
    img_data = buf.read()

    # Generate a PDF from the template
    pdf_data = render_template('pdf_template.html', img_data=img_data)
    pdf = pdfkit.from_string(pdf_data, False)

    # Send the PDF as a response
    response = send_file(BytesIO(pdf), attachment_filename='inventory_report.pdf', as_attachment=True)
    response.headers['Content-Type'] = 'application/pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)