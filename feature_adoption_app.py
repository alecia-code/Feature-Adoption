# Feature Adoption Dashboard using Plotly Dash

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("feature_adoption_dataset.csv")
df["signup_date"] = pd.to_datetime(df["signup_date"])

# Initialize app
app = dash.Dash(__name__)
app.title = "Feature Adoption Dashboard"

app.layout = html.Div([
    html.H1("Feature Adoption Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Device Type"),
        dcc.Dropdown(
            options=[{"label": d, "value": d} for d in df["device_type"].unique()],
            multi=True,
            id="device-filter",
            placeholder="Select device types"
        ),

        html.Label("Channel"),
        dcc.Dropdown(
            options=[{"label": c, "value": c} for c in df["channel"].unique()],
            multi=True,
            id="channel-filter",
            placeholder="Select channels"
        )
    ], style={"width": "40%", "margin": "auto"}),

    html.Br(),
    html.Div(id="kpi-banner", style={"textAlign": "center", "fontSize": "18px", "padding": "10px", "backgroundColor": "#f9f9f9"}),

    dcc.Graph(id="adoption-bar"),
    dcc.Graph(id="usage-boxplot"),
    dcc.Graph(id="heatmap")
])

@app.callback(
    [Output("adoption-bar", "figure"),
     Output("usage-boxplot", "figure"),
     Output("heatmap", "figure"),
     Output("kpi-banner", "children")],
    [Input("device-filter", "value"),
     Input("channel-filter", "value")]
)
def update_dashboard(devices, channels):
    dff = df.copy()
    if devices:
        dff = dff[dff["device_type"].isin(devices)]
    if channels:
        dff = dff[dff["channel"].isin(channels)]

    adoption_rate = dff["feature_adopted"].mean() * 100
    avg_usage = dff[dff["feature_adopted"] == 1]["feature_used_times"].mean()
    total_users = len(dff)
    adopted_users = dff["feature_adopted"].sum()

    kpi = f"Total Users: {total_users:,} | Adopted Users: {adopted_users:,} | Adoption Rate: {adoption_rate:.2f}% | Avg Uses: {avg_usage:.2f}"

    bar_fig = px.bar(
        dff.groupby("device_type")["feature_adopted"].mean().reset_index(),
        x="device_type", y="feature_adopted",
        title="Feature Adoption Rate by Device Type",
        labels={"feature_adopted": "Adoption Rate"}
    )

    box_fig = px.box(
        dff[dff["feature_adopted"] == 1],
        x="channel", y="feature_used_times",
        title="Feature Use Distribution by Channel",
        labels={"feature_used_times": "Times Used"}
    )

    heatmap_data = dff.groupby(["device_type", "channel"]).agg(
        adoption_rate=("feature_adopted", "mean")
    ).reset_index()

    heatmap_fig = px.density_heatmap(
        heatmap_data, x="channel", y="device_type", z="adoption_rate",
        color_continuous_scale="Blues", title="Adoption Rate Heatmap by Segment"
    )

    return bar_fig, box_fig, heatmap_fig, kpi

if __name__ == "__main__":
    app.run_server(debug=True)
