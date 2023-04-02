import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression

@st.cache_data
def pressure_difference_squared(df, pr):
    df['Pr2 - Pwf2'] = pr**2 - df['Pwf (psia)']**2
    return df

@st.cache_data
def plot_log_log_of_C(df, pr):

    # Create a log-log scatterplot
    fig = px.scatter(df, x="Qsc (Mscf/D)", y="Pr2 - Pwf2", log_x=True, log_y=True,
                     title="Log-log plot of Flow After Flow test")

    # Fit a regression line to the data
    X = df["Qsc (Mscf/D)"].values.reshape(-1, 1)
    y = df["Pr2 - Pwf2"].values.reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)

    # Add regression line to the plot
    fig.add_trace(go.Scatter(x=df["Qsc (Mscf/D)"], y=y_pred.flatten(),
                             mode='lines', name='Regression Line'))

    # # Add regression line formula to the plot
    # fig.add_annotation(x=0.05, y=0.95, xref='paper', yref='paper',
    #                    showarrow=False,
    #                    text=f"Regression line: y = {model.intercept_[0]:.2f} + {model.coef_[0][0]:.2f}x")

    return fig

@st.cache_data
def find_n(df):
    upper = np.log10(df['Qsc (Mscf/D)'].to_numpy()[0]) - np.log10(df['Qsc (Mscf/D)'].to_numpy()[-1])
    lower = np.log10(df['Pr2 - Pwf2'].to_numpy()[0]) - np.log10(df['Pr2 - Pwf2'].to_numpy()[-1])
    n = upper/lower
    return np.round(n,2)
