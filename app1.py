import pandas as pd
from flask import Flask, render_template, request
import json
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

# Load dataset
data_path = 'superstore.csv'  # Path to your dataset
df = pd.read_csv(data_path)

# Ensure correct data types for filtering
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Convert 'Year' to numeric, handle errors
df = df.dropna(subset=['Year', 'Category', 'Sales'])  # Drop rows with missing essential values

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get form values or default values
    selected_year = request.form.get('year', str(int(df['Year'].min())))  # Default to first year
    selected_category = request.form.get('category', df['Category'].unique()[0])  # Default to first category

    # Filter data
    filtered_data = df[(df['Year'] == int(selected_year)) & (df['Category'] == selected_category)]

    # Handle empty filtered data
    if filtered_data.empty:
        fig = px.bar(title="No data available for the selected filters.")
    else:
        # Create Plotly chart
        fig = px.bar(
            filtered_data,
            x='Category',
            y='Sales',
            title=f'Sales for {selected_category} in {selected_year}',
            labels={'Sales': 'Sales ($)', 'Category': 'Product Category'}
        )

    # Convert figure to JSON
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    # Get unique years and categories for dropdowns
    years = sorted(df['Year'].unique())
    categories = df['Category'].unique()

    return render_template(
        'index.html',
        graphJSON=graphJSON,
        years=years,
        categories=categories,
        selected_year=selected_year,
        selected_category=selected_category,
    )

if __name__ == '__main__':
    app.run(debug=True)
