
import streamlit as st
import requests
from pyvis.network import Network
import streamlit.components.v1 as components

# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Network Explorer",
    page_icon="🕸️",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🕸️ CrimeGraph AI — Network Explorer")
st.write("Explore relationships between entities in the CrimeGraph network.")

# ============================================================
# GET NETWORK DATA
# ============================================================

try:
    response = requests.get(
        f"{BACKEND_URL}/api/network",
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

except requests.exceptions.ConnectionError:
    st.error("❌ Backend is not running.")
    st.info(
        "Start the backend first with: "
        "`python backend\\api.py`"
    )
    st.stop()

except requests.exceptions.Timeout:
    st.error("❌ Backend request timed out.")
    st.stop()

except requests.exceptions.RequestException as e:
    st.error("❌ Could not connect to the backend.")
    st.code(str(e))
    st.stop()

except Exception as e:
    st.error("❌ Unexpected error.")
    st.code(str(e))
    st.stop()

# ============================================================
# DATA
# ============================================================

nodes = data.get("nodes", [])
edges = data.get("edges", [])

node_count = data.get(
    "node_count",
    len(nodes)
)

edge_count = data.get(
    "edge_count",
    len(edges)
)

# ============================================================
# SUMMARY
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👤 Network Entities",
        node_count
    )

with col2:
    st.metric(
        "🔗 Relationships",
        edge_count
    )

with col3:
    st.metric(
        "📊 Network Status",
        "Active"
    )

st.divider()

# ============================================================
# EMPTY NETWORK CHECK
# ============================================================

if not nodes:
    st.warning(
        "⚠️ No network entities were found in the backend data."
    )
    st.stop()

# ============================================================
# CREATE PYVIS GRAPH
# ============================================================

network = Network(
    height="700px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#000000",
    directed=False
)

network.barnes_hut(
    gravity=-30000,
    central_gravity=0.3,
    spring_length=150,
    spring_strength=0.05,
    damping=0.09
)

# ============================================================
# ADD NODES
# ============================================================

for node in nodes:

    node_id = str(
        node.get("id", "")
    )

    label = str(
        node.get(
            "label",
            node_id
        )
    )

    node_type = str(
        node.get(
            "type",
            "PERSON"
        )
    )

    connections = node.get(
        "connections",
        0
    )

    title = (
        f"<b>{label}</b><br>"
        f"ID: {node_id}<br>"
        f"Type: {node_type}<br>"
        f"Connections: {connections}"
    )

    network.add_node(
        node_id,
        label=label,
        title=title,
        size=max(
            15,
            min(
                40,
                15 + connections * 3
            )
        )
    )

# ============================================================
# ADD EDGES
# ============================================================

for edge in edges:

    source = str(
        edge.get("source", "")
    )

    target = str(
        edge.get("target", "")
    )

    relationship = str(
        edge.get(
            "relationship",
            "UNKNOWN"
        )
    )

    weight = edge.get(
        "weight",
        1
    )

    transaction_amount = edge.get(
        "transaction_amount",
        0
    )

    title = (
        f"Relationship: {relationship}<br>"
        f"Weight: {weight}<br>"
        f"Transaction amount: ₹{transaction_amount:,.2f}"
    )

    network.add_edge(
        source,
        target,
        value=max(
            1,
            float(weight)
        ),
        title=title
    )

# ============================================================
# GRAPH OPTIONS
# ============================================================

network.set_options(
    """
    {
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true,
          "iterations": 1000
        }
      },
      "nodes": {
        "shape": "dot",
        "font": {
          "size": 16
        }
      },
      "edges": {
        "smooth": true,
        "arrows": {
          "to": {
            "enabled": false
          }
        }
      }
    }
    """
)

# ============================================================
# DISPLAY GRAPH
# ============================================================

try:

    graph_html = network.generate_html()

    components.html(
        graph_html,
        height=720,
        scrolling=True
    )

except Exception as e:

    st.error(
        "❌ Could not render the network graph."
    )

    st.code(str(e))

# ============================================================
# RAW NETWORK DATA
# ============================================================

with st.expander("🔍 View Network Data"):

    st.write(
        f"**Nodes:** {node_count}"
    )

    st.write(
        f"**Edges:** {edge_count}"
    )

    st.json(data)



