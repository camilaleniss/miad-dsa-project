import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

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

    # Optional: Group smaller categories into an "Other" category for clarity
    top_n = 10  # Show only the top 10 weapon descriptions
    if len(weapon_counts) > top_n:
        others = weapon_counts[top_n:].sum()
        weapon_counts = pd.concat([weapon_counts[:top_n], pd.Series({"Other": others})])

    # Create a pie chart with plotly.express
    fig = px.pie(
        names=weapon_counts.index,
        values=weapon_counts.values,
        title="Distribution of Weapon Used",
        color_discrete_sequence=px.colors.sequential.Tealgrn_r  
    )

    # Update layout for improved readability and aesthetics
    fig.update_traces(
        textinfo='percent+label',  # Show percentages and labels
        pull=[0.1 if i == 0 else 0 for i in range(len(weapon_counts))],  # Pull out the largest slice for emphasis
        rotation=45  # Rotate chart for better initial visibility
    )
    
    fig.update_layout(
        title={
            "text": "Distribution of Weapon Descriptions",
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "yanchor": "top",
            "font": {
                "size": 20,  # Increase the font size for the title
                "color": "#333"
            }
        },
        font=dict(size=10, color="#333"), 
        legend=dict(
            title="Weapon Types",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=-0.3,
            font=dict(size=12)
        ),
        margin=dict(t=50, b=50, l=50, r=50)  # Add padding for a clean look
    )

    return fig

# Dashboard layout
app.layout = html.Div(
    children=[
        html.H1("Crimes in USA"),
        dcc.Graph(
            id="weapon_desc_pie_chart",
            figure=plot_weapon_desc(data)  # Set initial figure to display
        )
    ]
)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
