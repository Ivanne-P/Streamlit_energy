import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load data
p3g5 = pd.read_csv("p3g5.csv")

# Region order
region_order = ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire", 
                "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France",
                "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire",
                "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]

# Colors
colors = {'ConsumptionMWh': 'blue', 'ProductionMWh': 'lightblue'}

# Init figure
fig = go.Figure()
legend_flags = {'ConsumptionMWh': False, 'ProductionMWh': False}

# Add one box per region+flow
for flow in ['ConsumptionMWh', 'ProductionMWh']:
    flow_data = p3g5[p3g5['Flow'] == flow]
    for _, row in flow_data.iterrows():
        synthetic = [row['min'], row['q2'], row['mean'], row['q3'], row['max']] * 20
        fig.add_trace(go.Box(
            y=synthetic,
            x=[row['Region']] * len(synthetic),
            name=flow.replace('MWh', ''),
            marker=dict(color=colors[flow], line=dict(width=0.7)),
            opacity=1,
            width=0.4,
            boxpoints=False,
            showlegend=not legend_flags[flow]
        ))
        legend_flags[flow] = True

# Layout
fig.update_layout(
    title="Electricity Consumption and Production by Region",
    width=1000,
    height=600,
    plot_bgcolor="rgba(240, 242, 246, 0.8)",
    boxmode="group",
    xaxis=dict(
        title="Region",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        tickangle=315,
        categoryorder='array',
        categoryarray=region_order
    ),
    yaxis=dict(
        title="Electricity (MWh)",
        range=[-500, 12000],
        tickformat="d",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        fixedrange=True,
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=1
    ),
    legend_title="Energy sources"
)

st.plotly_chart(fig)


### REVERSE CODE

# Define region order
region_order = ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire", 
                "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France",
                "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire",
                "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]

# Define colors
colors = {'ConsumptionMWh': 'blue', 'ProductionMWh': 'lightblue'}

# Init figure
fig = go.Figure()

# Add one box per region+flow using synthetic data from summary stats
for flow in ['ConsumptionMWh', 'ProductionMWh']:
    flow_data = p3g5[p3g5['Flow'] == flow]
    for _, row in flow_data.iterrows():
        synthetic = [row['min'], row['q2'], row['mean'], row['q3'], row['max']] * 20
        fig.add_trace(go.Box(
        y=synthetic,
        x=[row['Region']] * len(synthetic),
        name=flow.replace('MWh', ''),
        marker=dict(color=colors[flow], line=dict(width=0.7)),
        opacity=1,
        width=0.6,
        boxpoints=False,
        showlegend=not legend_flags[flow]
))

# Add 2 dummy traces for legend only
for flow in ['ConsumptionMWh', 'ProductionMWh']:
    fig.add_trace(go.Box(
        y=[None],
        name=flow.replace('MWh', ''),
        marker=dict(color=colors[flow]),
        showlegend=True
    ))

# Layout
fig.update_layout(
    title="Electricity Consumption and Production by Region",
    width=1200,
    height=600,
    plot_bgcolor="rgba(240, 242, 246, 0.8)",
    boxmode="group",
    xaxis=dict(
        title="Region",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        tickangle=315,
        categoryorder='array',
        categoryarray=region_order
    ),
    yaxis=dict(
        title="Electricity (MWh)",
        range=[-500, 12000],
        tickformat="d",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        fixedrange=True,
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=1
    ),
    legend_title="Energy sources"
)

# Display in Streamlit
st.plotly_chart(fig)



### NEW ATTEMPT
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load data
p3g5 = pd.read_csv("p3g5.csv")

# Define region order
region_order = ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire", 
                "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France",
                "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire",
                "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]

# Define colors
colors = {'ConsumptionMWh': 'blue', 'ProductionMWh': 'lightblue'}

# Create figure
fig = go.Figure()
legend_flags = {'ConsumptionMWh': False, 'ProductionMWh': False}

# Add boxplots with adjusted x-labels
for flow in ['ConsumptionMWh', 'ProductionMWh']:
    flow_data = p3g5[p3g5['Flow'] == flow]
    for _, row in flow_data.iterrows():
        synthetic = [row['min'], row['q2'], row['mean'], row['q3'], row['max']] * 20
        region_flow_label = f"{row['Region']} - {flow}"
        fig.add_trace(go.Box(
            y=synthetic,
            x=[region_flow_label] * len(synthetic),
            name=flow.replace('MWh', ''),
            marker=dict(color=colors[flow], line=dict(width=0.7)),
            opacity=1,
            width=0.6,
            boxpoints=False,
            showlegend=not legend_flags[flow]
        ))
        legend_flags[flow] = True

# Set tick values and clean labels
tickvals = [f"{r} - ConsumptionMWh" for r in region_order]
ticktext = region_order

# Layout
fig.update_layout(
    title="Electricity Consumption and Production by Region 3",
    width=1200,
    height=600,
    plot_bgcolor="rgba(240, 242, 246, 0.8)",
    boxmode="group",
    xaxis=dict(
        title="Region",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        tickangle=315,
        tickvals=tickvals,
        ticktext=ticktext,
        categoryorder='array',
        categoryarray=tickvals + [f"{r} - ProductionMWh" for r in region_order]
    ),
    yaxis=dict(
        title="Electricity (MWh)",
        range=[-500, 12000],
        tickformat="d",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        fixedrange=True,
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=1
    ),
    legend_title="Energy sources"
)

# Display in Streamlit
st.plotly_chart(fig)

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load data
p3g5 = pd.read_csv("p3g5.csv")

# Define region order
region_order = ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire", 
                "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France",
                "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire",
                "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]

# Define colors
colors = {'ConsumptionMWh': 'blue', 'ProductionMWh': 'lightblue'}

# Init figure
fig = go.Figure()
legend_flags = {'ConsumptionMWh': False, 'ProductionMWh': False}

# Add one trace per region+flow
for flow in ['ConsumptionMWh', 'ProductionMWh']:
    flow_data = p3g5[p3g5['Flow'] == flow]
    for _, row in flow_data.iterrows():
        synthetic = [row['min'], row['q2'], row['mean'], row['q3'], row['max']] * 20
        fig.add_trace(go.Box(
            y=synthetic,
            x=[row['Region']] * len(synthetic),
            name=flow.replace('MWh', ''),
            marker=dict(color=colors[flow], line=dict(width=0.7)),
            opacity=1,
            width=0.6,
            boxpoints=False,
            showlegend=not legend_flags[flow]
        ))
        legend_flags[flow] = True

# Layout
fig.update_layout(
    title="Electricity Consumption and Production by Region 4",
    width=1200,
    height=600,
    plot_bgcolor="rgba(240, 242, 246, 0.8)",
    boxmode="group",
    xaxis=dict(
        title="Region",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        tickangle=315,
        categoryorder='array',
        categoryarray=region_order
    ),
    yaxis=dict(
        title="Electricity (MWh)",
        range=[-500, 12000],
        tickformat="d",
        showgrid=True,
        gridcolor="gray",
        gridwidth=1,
        griddash="dot",
        fixedrange=True,
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=1
    ),
    legend_title="Energy sources"
)

# Show in Streamlit
st.plotly_chart(fig)



    # Set the order of the regions
    region_order = ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire",
                    "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France",
                    "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire",
                    "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]

    # Set the style of the seaborn plot
    sns.set(style="whitegrid")

    # Create the plot
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x="Region", y="Value", hue="Type", data=p3g5,
                     order=region_order, showfliers=False)

    # Customize the plot
    ax.set_title("Electricity Consumption and Production by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Electricity (MWh)")
    ax.set_ylim(-500, 12000)
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=1)
    ax.legend(title="Energy sources")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Display the plot in Streamlit
    st.pyplot(plt)