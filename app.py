import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Initialize the app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard - USA Crimes"
server = app.server

# Load data from CSV
def load_data():
    data = pd.read_csv('data/Crime_Data_from_2020_to_Present.csv')
    return data

# Load the dataset
data = load_data()

# Generate pie chart for 'Weapon Desc' variable
def plot_weapon_desc(data):
    # Count the occurrences of each weapon description
    weapon_counts = data['Weapon Desc'].value_counts()
    
    # Create a pie chart figure
    fig = go.Figure(
        go.Pie(
            labels=weapon_counts.index,
            values=weapon_counts.values,
            hole=.3  # Optional: To create a donut-style chart
        )
    )

    fig.update_layout(
        title="Distribution of Weapon Descriptions",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#2cfec1"
    )
    
    return fig


# Dashboard layout
app.layout = html.Div(
    children=[
        html.H1("Weapon Description Dashboard"),
        dcc.Graph(
            id="weapon_desc_pie_chart",
            figure=plot_weapon_desc(data)  # Set initial figure to display
        )
    ]
)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
