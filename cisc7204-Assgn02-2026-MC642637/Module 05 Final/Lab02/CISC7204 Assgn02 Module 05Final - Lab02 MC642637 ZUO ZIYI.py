#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CISC7204 Assignment 02 - Module 05 Final Project, Part 2.

Interactive automobile sales dashboards for yearly and recession reports.
Run this file from any working directory; the CSV is loaded relative to it.
"""

from pathlib import Path

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "automobile-sales.csv"
data = pd.read_csv(DATA_FILE)

# Keep the month chart in calendar order rather than alphabetic order.
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
data["Month"] = pd.Categorical(data["Month"], categories=MONTHS, ordered=True)

year_list = sorted(data["Year"].dropna().astype(int).unique().tolist())
statistics_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]

app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

CONTROL_STYLE = {"width": "min(80%, 720px)", "margin": "12px auto", "fontSize": "18px"}
GRAPH_STYLE = {"minWidth": 0, "width": "100%"}
GRID_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
    "gap": "16px",
    "alignItems": "stretch",
}

app.layout = html.Main(
    [
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": "24px", "margin": "24px"},
        ),
        html.Div(
            [
                html.Label("Select Statistics:", htmlFor="dropdown-statistics"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=statistics_options,
                    value=None,
                    placeholder="Select a report type",
                    clearable=False,
                    style=CONTROL_STYLE,
                ),
            ],
            style={"textAlign": "center", "marginBottom": "16px"},
        ),
        html.Div(
            [
                html.Label("Select Year:", htmlFor="select-year"),
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": year, "value": year} for year in year_list],
                    value=None,
                    placeholder="Select year",
                    clearable=False,
                    disabled=True,
                    style=CONTROL_STYLE,
                ),
            ],
            style={"textAlign": "center", "marginBottom": "24px"},
        ),
        html.Div(id="output-container", className="chart-grid", style=GRID_STYLE),
    ],
    style={"maxWidth": "1500px", "margin": "0 auto", "padding": "12px"},
)


@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    """Enable year selection only for the yearly report."""
    return selected_statistics != "Yearly Statistics"


@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="select-year", component_property="value"),
    ],
)
def update_output_container(selected_statistics, input_year):
    """Build the four charts for the selected report."""
    if selected_statistics == "Recession Period Statistics":
        recession_data = data.loc[data["Recession"].eq(1)].copy()

        yearly_rec = (
            recession_data.groupby("Year", as_index=False, observed=True)["Automobile_Sales"]
            .mean()
        )
        chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                markers=True,
                title="Average Automobile Sales During Recession Periods",
                labels={"Automobile_Sales": "Average automobile sales"},
            ),
            style=GRAPH_STYLE,
        )

        average_sales = (
            recession_data.groupby("Vehicle_Type", as_index=False, observed=True)["Automobile_Sales"]
            .mean()
            .sort_values("Automobile_Sales", ascending=False)
        )
        chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type During Recessions",
                labels={"Vehicle_Type": "Vehicle type", "Automobile_Sales": "Average sales"},
            ),
            style=GRAPH_STYLE,
        )

        expenditure = (
            recession_data.groupby("Vehicle_Type", as_index=False, observed=True)["Advertising_Expenditure"]
            .sum()
        )
        chart3 = dcc.Graph(
            figure=px.pie(
                expenditure,
                names="Vehicle_Type",
                values="Advertising_Expenditure",
                title="Advertising Expenditure Share by Vehicle Type During Recessions",
            ),
            style=GRAPH_STYLE,
        )

        unemployment_sales = (
            recession_data.groupby(["unemployment_rate", "Vehicle_Type"], as_index=False, observed=True)
            ["Automobile_Sales"].mean()
        )
        chart4 = dcc.Graph(
            figure=px.bar(
                unemployment_sales,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                barmode="group",
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
                labels={
                    "unemployment_rate": "Unemployment rate (%)",
                    "Automobile_Sales": "Average automobile sales",
                    "Vehicle_Type": "Vehicle type",
                },
            ),
            style=GRAPH_STYLE,
        )
        return [chart1, chart2, chart3, chart4]

    if selected_statistics == "Yearly Statistics" and input_year is not None:
        input_year = int(input_year)
        yearly_data = data.loc[data["Year"].eq(input_year)].copy()

        yearly_sales = data.groupby("Year", as_index=False, observed=True)["Automobile_Sales"].mean()
        chart1 = dcc.Graph(
            figure=px.line(
                yearly_sales,
                x="Year",
                y="Automobile_Sales",
                markers=True,
                title="Average Yearly Automobile Sales, 1980–2023",
                labels={"Automobile_Sales": "Average automobile sales"},
            ),
            style=GRAPH_STYLE,
        )

        monthly_sales = (
            yearly_data.groupby("Month", as_index=False, observed=True)["Automobile_Sales"]
            .sum()
            .sort_values("Month")
        )
        chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x="Month",
                y="Automobile_Sales",
                markers=True,
                title=f"Total Monthly Automobile Sales in {input_year}",
                labels={"Month": "Month", "Automobile_Sales": "Total automobile sales"},
            ),
            style=GRAPH_STYLE,
        )

        vehicle_sales = (
            yearly_data.groupby("Vehicle_Type", as_index=False, observed=True)["Automobile_Sales"]
            .mean()
            .sort_values("Automobile_Sales", ascending=False)
        )
        chart3 = dcc.Graph(
            figure=px.bar(
                vehicle_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}",
                labels={"Vehicle_Type": "Vehicle type", "Automobile_Sales": "Average sales"},
            ),
            style=GRAPH_STYLE,
        )

        yearly_expenditure = (
            yearly_data.groupby("Vehicle_Type", as_index=False, observed=True)["Advertising_Expenditure"]
            .sum()
        )
        chart4 = dcc.Graph(
            figure=px.pie(
                yearly_expenditure,
                names="Vehicle_Type",
                values="Advertising_Expenditure",
                title=f"Advertising Expenditure by Vehicle Type in {input_year}",
            ),
            style=GRAPH_STYLE,
        )
        return [chart1, chart2, chart3, chart4]

    return html.Div("Select a report type to display the dashboard.", style={"padding": "24px"})


if __name__ == "__main__":
    app.run(debug=True)
