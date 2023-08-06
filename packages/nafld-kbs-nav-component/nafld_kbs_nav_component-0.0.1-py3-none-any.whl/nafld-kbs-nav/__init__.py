import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
  _component_func = components.declare_component(
    "nafld_kbs_nav",
    url="http://localhost:3000", # vite dev server port
  )
else:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend/dist")
  _component_func = components.declare_component("nafld_kbs_nav", path=build_dir)

def nafld_kbs_nav(name, key=None):
  component_value = _component_func(name=name, key=key, default=0)
  return component_value

if not _RELEASE:
  import streamlit as st
  st.subheader("Component Test")
  num_clicks = nafld_kbs_nav(name = "NameViteVue")
  st.markdown("You've clicked %s times!" % int(num_clicks))