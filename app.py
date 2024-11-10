import dash
from dash import dcc
from dash import html
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
    data['Offense Severity'] = data['Part 1-2'].map({1: "Serious", 2: "Less Serious"})
    return data

# Load the dataset
data = load_data()

def sample_data(data, sample_size=10000):
    if len(data) > sample_size:
        data = data.sample(n=sample_size, random_state=42)  # Randomly sample rows
    return data

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
                "size": 20, 
                "color": "#333"
            }
        },
        font=dict(size=10, color="#333"), 
        legend=dict(
            title="Weapon Types",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=-5.5,
            font=dict(size=12)
        ),
        margin=dict(t=50, b=50, l=50, r=50)  # Add padding for a clean look
    )

    return fig

# Generate histogram for 'Part 1-2' column
def plot_part_1_2_histogram(data):
    fig = px.histogram(
        data,
        x='Offense Severity',
        color='Offense Severity',  # Color by category to differentiate Part 1 and Part 2
        title="Frequency of Serious and Less Serious Offenses",
        color_discrete_map={"Serious": "#2C98A0", "Less serious": "#B0F2BC"}  # Custom colors for clarity
    )

    # Update layout for readability
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Offense Severity",
        yaxis_title="Count",
        font=dict(size=12, color="#333"),
        legend=dict(title="Offense Type", font=dict(size=10)),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

# Generate histogram for 'Vict Sex' column
def plot_vict_sex_histogram(data):
    fig = px.histogram(
        data,
        x='Vict Sex',
        color='Vict Sex',
        title="Distribution of Victim Sex",
        color_discrete_sequence=px.colors.sequential.Tealgrn_r
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_title="Victim Sex",
        yaxis_title="Count",
        font=dict(size=12, color="#333"),
        legend=dict(title="Victim Sex", font=dict(size=10)),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

# Generate histogram for 'Vict Age' column
def plot_vict_age_histogram(data):
    fig = px.histogram(
        data,
        x='Vict Age',
        title="Distribution of Victim Age",
        nbins=20,  # Adjust number of bins for age grouping
        color_discrete_sequence=px.colors.sequential.Tealgrn_r
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_title="Victim Age",
        yaxis_title="Count",
        font=dict(size=12, color="#333"),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

def plot_density_map(data):
    data_used = sample_data(data, 10000)
    # Ensure the columns for latitude and longitude are available
    if 'LAT' not in data_used.columns or 'LON' not in data_used.columns:
        raise ValueError("LAT and LON columns are required for the map.")

    # Create the map with scatter_mapbox
    fig = px.density_mapbox(
        data_used,
        lat="LAT",
        lon="LON",
        hover_name="AREA NAME",  # Optional: display other info on hover
        color_continuous_scale="Tealgrn_r",  
        title="Crime Density Map",
        opacity=0.6,  # Adjust opacity of the points
        height=600
    )

    # Update map layout for a more interactive look
    fig.update_layout(
        mapbox_style="open-street-map",  # Set the map style (you can use other options like 'carto-positron')
        mapbox_zoom=10,  # Initial zoom level
        mapbox_center={"lat": 34.0522, "lon": -118.2437}, # Center in LA
        font=dict(size=12, color="#333"),
        margin={"r": 0, "t": 40, "l": 0, "b": 0}  # Adjust margins for a cleaner view
    )

    return fig

# Update app layout with arranged graphs
app.layout = html.Div(
    children=[
        html.H1("Crimes in USA",
                style={
                "textAlign": "center",  # Center the title
                "fontSize": 30,  # Adjust the font size
                "color": "#333",  # Set the color to match the chart titles
                "marginTop": 20,  # Space above the title
                "fontFamily": "Arial, sans-serif"  # Use the same font family as the charts
            }),
        html.Div(
            children=[
                dcc.Graph(
                    id="density_map",
                    figure=plot_density_map(data),  # Density map for LAT/LON
                    style={"width": "75%"}
                ),
                dcc.Graph(
                    id="part_1_2_histogram",
                    figure=plot_part_1_2_histogram(data),  # Histogram for Offense Severity
                    style={"width": "35%"} 
                )
            ],
            style={"display": "flex", "justify-content": "space-between"}
        ),
        dcc.Graph(
                    id="weapon_desc_pie_chart",
                    figure=plot_weapon_desc(data),  # Pie chart for Weapon Desc
                ),
        html.Div(
            children=[
                dcc.Graph(
                    id="vict_sex_histogram",
                    figure=plot_vict_sex_histogram(data)  # Histogram for Victim Sex
                ),
                dcc.Graph(
                    id="vict_age_histogram",
                    figure=plot_vict_age_histogram(data)  # Histogram for Victim Age
                )
            ],
           style={
                "display": "flex",
                "justify-content": "center",  # Center the histograms
                "gap": "2rem",  # Add space between the graphs
                "width": "80%",  # Set a maximum width for better alignment
                "margin": "0 auto"  # Center the container div
            }
        ) 
    ]
)

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
