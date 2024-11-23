# Prueba de API dashboard
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests

# Initialize the app
app = dash.Dash(__name__)

app.title = "Crime Prediction Dashboard"
server = app.server

# Layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Crime Prediction Dashboard", style={"textAlign": "center", "fontSize": 30}),
        
        # Form for the user to enter data
        html.Div(
            children=[
                html.Label("AREA:"),
                dcc.Input(id='area', type='number', step='any', placeholder="Enter AREA", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Rpt_Dist_No:"),
                dcc.Input(id='rpt_dist_no', type='number', step='any', placeholder="Enter Report District No.", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Crm_Cd:"),
                dcc.Input(id='crm_cd', type='number', step='any', placeholder="Enter Crime Code", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Vict_Age:"),
                dcc.Input(id='vict_age', type='number', step='any', placeholder="Enter Victim Age", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Premis_Cd:"),
                dcc.Input(id='premis_cd', type='number', step='any', placeholder="Enter Premises Code", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Status:"),
                dcc.Input(id='status', type='number', step='any', placeholder="Enter Status", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Status_Desc:"),
                dcc.Input(id='status_desc', type='number', step='any', placeholder="Enter Status Description", style={"width": "50%"}),
                html.Br(),
                
                html.Label("Crm_Cd_1:"),
                dcc.Input(id='crm_cd_1', type='number', step='any', placeholder="Enter Crime Code 1", style={"width": "50%"}),
                html.Br(),
                
                html.Label("LAT:"),
                dcc.Input(id='lat', type='number', step='any', placeholder="Enter Latitude", style={"width": "50%"}),
                html.Br(),
                
                html.Label("LON:"),
                dcc.Input(id='lon', type='number', step='any', placeholder="Enter Longitude", style={"width": "50%"}),
                html.Br(),
                
                # Button to submit the form
                html.Button('Get Prediction', id='predict_button', n_clicks=0),
                html.Div(id='prediction_output', style={"marginTop": "20px", "fontSize": "18px"})
            ],
            style={"textAlign": "center", "marginTop": "20px"}
        ),
    ]
)

# Function to call the API and get the prediction
def get_prediction(data):
    # URL of the API endpoint
    api_url = "http://127.0.0.1:8000/predict"  # Replace with your actual FastAPI URL if needed
    
    # Create payload to send to the API
    payload = {
        "AREA": data['AREA'],
        "Rpt_Dist_No": data['Rpt_Dist_No'],
        "Crm_Cd": data['Crm_Cd'],
        "Vict_Age": data['Vict_Age'],
        "Premis_Cd": data['Premis_Cd'],
        "Status": data['Status'],
        "Status_Desc": data['Status_Desc'],
        "Crm_Cd_1": data['Crm_Cd_1'],
        "LAT": data['LAT'],
        "LON": data['LON']
    }
    
    try:
        # Make the API request
        response = requests.post(api_url, json=payload)
        
        # If the request is successful
        if response.status_code == 200:
            prediction = response.json()  # Get the prediction from the response
            return prediction['prediction']  # Assuming the API returns a key 'prediction'
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Callback to handle the prediction request when the button is clicked
@app.callback(
    Output('prediction_output', 'children'),
    Input('predict_button', 'n_clicks'),
    State('area', 'value'),
    State('rpt_dist_no', 'value'),
    State('crm_cd', 'value'),
    State('vict_age', 'value'),
    State('premis_cd', 'value'),
    State('status', 'value'),
    State('status_desc', 'value'),
    State('crm_cd_1', 'value'),
    State('lat', 'value'),
    State('lon', 'value')
)
def update_prediction(n_clicks, area, rpt_dist_no, crm_cd, vict_age, premis_cd, status, status_desc, crm_cd_1, lat, lon):
    if n_clicks > 0:
        # Create the data dictionary from user input
        input_data = {
            "AREA": float(area) if area else 0.0,
            "Rpt_Dist_No": float(rpt_dist_no) if rpt_dist_no else 0.0,
            "Crm_Cd": float(crm_cd) if crm_cd else 0.0,
            "Vict_Age": float(vict_age) if vict_age else 0.0,
            "Premis_Cd": float(premis_cd) if premis_cd else 0.0,
            "Status": float(status) if status else 0.0,
            "Status_Desc": float(status_desc) if status_desc else 0.0,
            "Crm_Cd_1": float(crm_cd_1) if crm_cd_1 else 0.0,
            "LAT": float(lat) if lat else 0.0,
            "LON": float(lon) if lon else 0.0
        }
        
        prediction = get_prediction(input_data)

        # Diccionario de mapeo de predicción
        prediction_map = {1: "Serious", 2: "Less Serious"}

        # Mapear la predicción a la descripción y devolver la respuesta
        prediction_description = prediction_map.get(prediction, "Unknown Prediction")
        return f"Prediction: {prediction_description}"
    
    return "Enter the data and click 'Get Prediction'"

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
