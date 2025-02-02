from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

# Sample sales data
data = {
    'Year': [2022, 2022, 2022, 2023, 2023, 2023, 2024, 2024, 2024],
    'Category': ['Electronics', 'Furniture', 'Clothing'] * 3,
    'Sales': [200, 150, 100, 250, 200, 150, 300, 250, 200],
}
df = pd.DataFrame(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get filter values from the form
    selected_year = request.form.get('year', '2022')  # Default to 2022
    selected_category = request.form.get('category', 'Electronics')  # Default category

    # Debugging: Print selected filters
    print(f"Selected Year: {selected_year}, Selected Category: {selected_category}")

    # Filter the DataFrame
    try:
        filtered_data = df[(df['Year'] == int(selected_year)) & (df['Category'] == selected_category)]
        # Debugging: Print filtered data
        print("Filtered Data:")
        print(filtered_data)
    except Exception as e:
        print(f"Error during filtering: {e}")
        filtered_data = pd.DataFrame()  # Empty DataFrame to avoid crashes

    # Create a Plotly chart (only if filtered_data has rows)
    if not filtered_data.empty:
        fig = px.bar(
            filtered_data,
            x='Category',
            y='Sales',
            title=f'Sales for {selected_category} in {selected_year}',
            labels={'Sales': 'Sales ($)', 'Category': 'Product Category'}
        )
        # Convert the figure to JSON
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    else:
        graphJSON = None  # No data to plot

    # Get unique years and categories for dropdowns
    years = sorted(df['Year'].unique())
    categories = df['Category'].unique()

    return render_template(
        'home.html',
        graphJSON=graphJSON,
        years=years,
        categories=categories,
        selected_year=selected_year,
        selected_category=selected_category,
    )

if __name__ == '__main__':
    app.run(debug=True)
