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
    

    if st.button("Clear state"):
        state.clear()
#    if st.button("Save State File"):
#        with open("binary_list.bin", "wb") as filename:
#            dill.dump(state._state['data'], filename)
#    if st.button("Load State File"):
#        with open("binary_list.bin", "rb") as pickle_file:
#            state._state['data'] = dill.load(pickle_file)
        
        
        
    # Setup file uploader (for .csv)
    
        
#    state.file = st.file_uploader(label="Upload your bin", type =['bin'])
    state.uploadedFile = st.file_uploader(label="Upload your csv", type =['csv'])
    if state.uploadedFile is not None:
        state.dfUp = process_uploaded_file(state)
        
    
         
        
    display_state_values(state)
    
def process_uploaded_file(state):
    try:
        processedFile = pd.read_csv(state.uploadedFile, encoding='UTF-8')
    except:
        print("Error")
    
    return processedFile

def display_state_values(state):

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