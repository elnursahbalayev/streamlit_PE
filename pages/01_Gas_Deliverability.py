import streamlit as st
from functions.gas_deliverability import Radius_of_investigation
import numpy as np

requirement = st.selectbox('What do you want to calculate?',['Radius of investigation'])

if requirement == 'Radius of investigation':
    st.write('Please input the necessary data below')
    k = st.number_input('Permeability k(mD)', format='%f')
    pr = st.number_input('Average reservoir pressure (psia)', format='%f')
    fi = st.number_input('Porosity', format='%f')
    mu = st.number_input('Viscosity (cP)', format='%f')
    re = st.number_input('Reservoir boundary (ft)', format='%f')
    t = st.number_input('Time passed', format='%f')

    if 0 not in (k, pr, fi, mu, re, t):
        ts = Radius_of_investigation.calculate_stabilization_time(k, pr, fi, mu, re, t)
        rinv = Radius_of_investigation.calculate_radius_of_investigation(k, pr, t, fi, mu, ts, re)

        st.latex(r't_s = \frac{1000 \cdot \phi \cdot \mu \cdot r_e^2}{k \cdot p_R}')
        st.latex(f't_s = \\frac{{1000 \\cdot {fi} \\cdot {mu} \\cdot {re}^2}}{{{k} \\cdot {pr}}}')
        st.latex(f't_s = {np.round(ts,3)} \\text{{ hours}}')
        st.write('\n')

        st.latex(r'r_\text{inv} = 0.032 \sqrt{\frac{k \cdot p_R \cdot t}{\phi \cdot \mu_g}}')
        st.latex(f'r_\\text{{inv}} = 0.032 \\sqrt{{\\frac{{{k} \\cdot {pr} \\cdot {t}}}{{{fi} \\cdot {mu}}}}}')
        st.latex(f'r_\\text{{inv}} = {np.round(rinv,2)} \\text{{ ft}}')
