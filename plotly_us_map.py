from urllib.request import urlopen
import json
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};Server=WIN-10-TEST;Database=WIN10TEST;UID=sa;PWD=#7862Ellis@c1p')
cursor = conn.cursor()

# count of vendors by state
sql = "select count(id) as [count], [state] " + \
        "from vendor " + \
        "where isnull(state, '') <> '' " + \
        "and state in ('AL','AR','AZ','CA', " + \
        "            'CO','CT','DC','DE', " + \
        "            'FL','GA','HI','IL', " + \
        "            'IN','KY','LA','MA', " + \
        "            'MD','MI','MN','MO', " + \
        "            'MT','NC','NE','NJ', " + \
        "            'NM','NV','NY','OH', " + \
        "            'OK','OR','PA','RI', " + \
        "            'SC','TN','TX','UT', " + \
        "            'VA','WA','WI') " + \
        "group by [state]"

# count of contacts by state
'''sql = "select count(id) as [count], [state] " + \
    "from customer " + \
    "where isnull(state, '') <> ''  " + \
    "and state in ('AL','AR','AZ','CA', " + \
    "			'CO','CT','DC','DE', " + \
    "			'FL','GA','HI','IL', " + \
    "			'IN','KY','LA','MA', " + \
    "			'MD','MI','MN','MO', " + \
    "			'MT','NC','NE','NJ', " + \
    "			'NM','NV','NY','OH', " + \
    "			'OK','OR','PA','RI', " + \
    "			'SC','TN','TX','UT', " + \
    "			'VA','WA','WI') " + \
    "group by [state] " + \
    "order by [state] "

# total in dollars, by state
sql = "select sum(total_amt_recvd) as [count], [state] " + \
    "from vendor " + \
    "inner join purchase_order on vendor.id = purchase_order.vendor_id " + \
    "where isnull(state, '') <> ''  " + \
    "and state in ('AL','AR','AZ','CA', " + \
    "			'CO','CT','DC','DE', " + \
    "			'FL','GA','HI','IL', " + \
    "			'IN','KY','LA','MA', " + \
    "			'MD','MI','MN','MO', " + \
    "			'MT','NC','NE','NJ', " + \
    "			'NM','NV','NY','OH', " + \
    "			'OK','OR','PA','RI', " + \
    "			'SC','TN','TX','UT', " + \
    "			'VA','WA','WI') " + \
    "group by [state] " + \
    "order by [state]"'''


# Choropleth visualization
# datasets found at https://github.com/plotly/datasets
# df = pd.read_csv("purchase_orders_by_state.csv", dtype={"state": str})  
df = pd.read_sql_query(sql, conn)

fig = go.Figure(data=go.Choropleth(
    locations=df['state'],          # Spatial coordinates
    z = df['count'].astype(float),  # Data to be color-coded
    locationmode = 'USA-states',    # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Vendor count",
))

fig.update_layout(
    title_text = 'CIP Vendors by State',
    geo_scope='usa', # limite map scope to USA
) 

fig.show()