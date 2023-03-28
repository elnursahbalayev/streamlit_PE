import streamlit as st
import numpy as np


@st.cache_data
def calculate_stabilization_time(k, pr, fi, mu, re, t):
    ts = 1000*fi*mu*(re**2)/(k*pr)
    return ts

@st.cache_data
def calculate_radius_of_investigation(k, pr, t, fi, mu, ts, re):
    if ts<=t:
        return re
    else:
        rinv = 0.032*np.sqrt(k*pr*t/(fi*mu))
        return rinv
