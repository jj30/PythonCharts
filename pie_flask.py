import pygal
from flask import Flask,render_template,request,session
from flask.templating import render_template
from pygal.style import Style
import pandas 
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};Server=WIN-10-TEST;Database=WIN10TEST;UID=sa;PWD=')
app = Flask(__name__)

def get_sizes():
    sql = "SELECT top 5 month(order_date) as month_ordered, year(order_date) as year_ordered, count(order_date) as number_orders, v.name, sum(total_amt_ordered) as total_amt_ordered " + \
            "FROM [WIN10TEST].[dbo].[PURCHASE_ORDER] " + \
            "inner join vendor v on v.id = vendor_id " + \
            "where year(order_date) = 2020 and month(order_date) = 1 " + \
            "group by v.name, month(order_date), year(order_date) " + \
            "order by number_orders desc"

    cursor = conn.cursor()
    cursor.execute(sql)

    idx = 0
    grand_total = 0
    list_pie_elems = []
    list_pie_names = []
    list_pie_fractions = []

    for row in cursor:
            idx += 1
            grand_total += row[2]

            list_pie_elems.append(row[2])
            list_pie_names.append(row[3])

    for i in range(idx):
            list_pie_fractions.append(list_pie_elems[i] / grand_total)

    return list_pie_names, list_pie_fractions

@app.route('/bar_route')   
def bar_route():
    try:
        '''bar_chart = pygal.Bar()
        bar_chart.title = 'Browser usage evolution (in %)'
        bar_chart.x_labels = map(str, range(2002, 2013))
        bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        bar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
        '''
        
        [labels, sizes] = get_sizes()

        bar_chart = pygal.Pie()
        bar_chart.title = 'Vendors by number of orders for January 2020 (in %)'

        for idx in range(len(labels)): 
            bar_chart.add(labels[idx], sizes[idx])

        '''bar_chart.add('Grainger', 19/191)
        bar_chart.add('McMaster-Carr', 17/191)
        bar_chart.add('Brevard Rigging Inc.', 14/191)
        bar_chart.add('Advantage Industrial Automation', 13/191)
        bar_chart.add('Other', 110/191)'''
            
        barchart_data=bar_chart.render_data_uri()
        return render_template('barchart.html',barchart_data=barchart_data)


    except Exception:
        return "error"