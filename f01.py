# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:30:29 2020

@author: apad
"""

import streamlit as st
from streamlit.hashing import _CodeHasher

import pandas as pd
import plotly.express as px

import dill


try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


def main():
    state = _get_state()
    pages = {
        "Dashboard": page_dashboard,
        "Settings": page_settings,
    }
    
    st.sidebar.title(":floppy_disk: Page states")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def page_dashboard(state):
    st.title(":chart_with_upwards_trend: Dashboard page")
    display_state_values(state)

def update_uploaded_file(state):
    pass
    

def page_settings(state):
    st.title(":wrench: Settings")
    

#    st.write("---")
#    options = ["Hello", "World", "Goodbye"]
#    state.input = st.text_input("Set input value.", state.input or "")
#    state.slider = st.slider("Set slider value.", 1, 10, state.slider)
#    state.radio = st.radio("Set radio value.", options, options.index(state.radio) if state.radio else 0)
#    state.checkbox = st.checkbox("Set checkbox value.", state.checkbox)
#    state.selectbox = st.selectbox("Select value.", options, options.index(state.selectbox) if state.selectbox else 0)
#    state.multiselect = st.multiselect("Select value(s).", options, state.multiselect)
#    
    if st.button("Clear state"):
        state.clear()
    if st.button("Save State File"):
        with open("binary_list.bin", "wb") as filename:
            dill.dump(state._state['data'], filename)
    if st.button("Load State File"):
        with open("binary_list.bin", "rb") as pickle_file:
            state._state['data'] = dill.load(pickle_file)
        
        
        
    # Setup file uploader (for .csv)
    
        
#    state.file = st.file_uploader(label="Upload your bin", type =['bin'])
    state.uploadedFile = st.file_uploader(label="Upload your csv", type =['csv'])
    if state.uploadedFile is not None:
        state.dfUp = process_uploaded_file(state)
        
    st.sidebar.title("Column Creation")
    state.newColCheckbox = st.sidebar.checkbox("Column creation?", state.newColCheckbox)
    
    
    if state.newColCheckbox:
        state.newColName = st.sidebar.text_input("Set column name:", state.newColName or "")
        state.dfUp[state.newColName] = 0
         
         
        state.newColContent1 = st.sidebar.selectbox("Select operand1 column", state.dfCols, state.dfCols.index(state.newColContent1) if state.newColContent1 else 0)
#             state.newColContent2 = st.sidebar.text_input("Operation2 for new column:", state.newColContent2 or "")
        operations = ["+", "-", "/", "*", "%100"]
        state.opRadio = st.sidebar.radio("Select operation type:", operations, operations.index(state.opRadio) if state.opRadio else 0)
    
        state.newColContent3 = st.sidebar.selectbox("Select operand2 column", state.dfCols, state.dfCols.index(state.newColContent3) if state.newColContent3 else 0)
         
        if state.opRadio == "+":
            state.dfUp[state.newColName] = state.dfUp[state.newColContent1] + state.dfUp[state.newColContent3]
            
        elif state.opRadio == "-":
            state.dfUp[state.newColName] = state.dfUp[state.newColContent1] - state.dfUp[state.newColContent3]
            
        elif state.opRadio == "/":
            state.dfUp[state.newColName] = state.dfUp[state.newColContent1] / state.dfUp[state.newColContent3]
            
        elif state.opRadio == "*":
            state.dfUp[state.newColName] = state.dfUp[state.newColContent1] * state.dfUp[state.newColContent3]
            
        elif state.opRadio == "%100":
            state.dfUp[state.newColName] = state.dfUp[state.newColContent1] / state.dfUp[state.newColContent3] * 100
            
                
        #state.dfCols =  state.dfUp.columns.tolist()

#            rstate.another = st.sidebar.selectbox("Select ANOTHER column", state.dfCols, state.dfCols.index(state.another) if state.another else 0)
        
    #st.sidebar.write("------------")
    st.sidebar.title("Graphic Options")
    state.hasGroups = False
    state.hasMultiColumns = False
    
#        maxColumns = len(dfUp.columns) -1
    state.dfCols =  state.dfUp.columns.tolist()
#        print(state.dfCols)

    state.xAxis = st.sidebar.selectbox("Select x Axis column", state.dfCols, state.dfCols.index(state.xAxis) if state.xAxis else 0)
    state.yAxis = st.sidebar.selectbox("Select y Axis column", state.dfCols, state.dfCols.index(state.yAxis) if state.yAxis else 0)
    
    if st.sidebar.button("Swap Axis"):
        tmp = state.xAxis
        state.xAxis = state.yAxis
        state.yAxis = tmp
    
    options = ['None', 'Groups', 'MultiVar']
    state.option = st.sidebar.radio("Select graphic option:", options, options.index(state.option) if state.option else 0)
    
    
    if state.option == 'Groups':
        state.group = st.sidebar.selectbox("Select grouping column", state.dfCols, state.dfCols.index(state.group) if state.group else 0)
        state.hasGroups = True
        
    
    elif state.option == 'MultiVar':
        state.multiColumns = st.sidebar.multiselect("Select multiple columns", state.dfCols, state.multiColumns)
        state.hasMultiColumns = True
        
        
    if st.sidebar.button("Make Graphic"):
        
        if state.hasGroups:
            
            
            state.fig = px.bar(state.dfUp, x=state.dfUp[state.xAxis], y=state.dfUp[state.yAxis], barmode='group', color=state.dfUp[state.group])
            
            
            
        elif state.hasMultiColumns:

            state.fig = px.bar(state.dfUp, x=state.multiColumns, y=state.dfUp[state.yAxis], text='value')

        else:
#                fig = px.pie(dfUp, names=dfUp[dfUp.columns[xAxis]], values=dfUp[dfUp.columns[yAxis]])
#                st.plotly_chart(fig)
            
            state.fig = px.bar(state.dfUp, x=state.dfUp[state.xAxis], y=state.dfUp[state.yAxis])

        #state.dfUp[state.newColName] = pd.eval(state.newColContent)
        #state.dfUp.Previstas*100
         
        
    display_state_values(state)
    
def process_uploaded_file(state):
    try:
        processedFile = pd.read_csv(state.uploadedFile, encoding='UTF-8')
    except:
        print("Error")
    
    return processedFile

def display_state_values(state):
#    st.write("Input state:", state.input)
#    st.write("Slider state:", state.slider)
#    st.write("Radio state:", state.radio)
#    st.write("Checkbox state:", state.checkbox)
#    st.write("Selectbox state:", state.selectbox)
#    st.write("Multiselect state:", state.multiselect)
#    
#    for i in range(3):
#        st.write(f"Value {i}:", state[f"State value {i}"])
#
#    if st.button("Clear state"):
#        state.clear()
    
        
    try:
        st.write("Uploaded file: ", state.uploadedFile.name)
    except:
        st.write("Uploaded file: None")
        

    try:
        st.dataframe(state.dfUp.style.set_precision(2))
    except:
        state.dfUp
    try:
        st.plotly_chart(state.fig)
    except:
        st.write("No graph")
    
    
            
class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()