import matplotlib.pyplot as plt
import cherrypy
import io
import numpy
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};Server=WIN-10-TEST;Database=WIN10TEST;Trusted_Connection=yes;')

# some code from https://gist.github.com/dukenmarga/6cb6bb8c650a5c77c488
class HelloWorld(object):
        @cherrypy.expose
        def index(self):
                # return plt.show()
                return ''' <img src="image.png" width="640" height="480" border="0" /> '''
                #return "HELLO WORLD"

        @cherrypy.expose
        def image_png(self):
                # img = self.createChart()
                img = io.BytesIO()
                self.plot(img)
                img.seek(0)
                return cherrypy.lib.static.serve_fileobj(img, content_type="png", name="image.png")

        def get_sizes(self):
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

        def plot(self, image):
                [labels, sizes] = self.get_sizes()
                # x = numpy.linspace(0, 10)
                # y = numpy.sin(x)
                # plt.plot(x, y)
                # plt.savefig(image, format='png')

                # code is from https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
                # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                # labels = 'Alro Metals', 'Grainger', 'McMaster-Carr', 'Brevard Rigging Inc.', 'Advantage Industrial Automation', 'Other'
                # sizes = [31/191, 19/191, 17/191, 14/191, 13/191, 110/191]
                explode = (0, 0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # pyplot.savefig(image, format='png')
                plt.savefig(image, format='png')

cherrypy.config.update({'server.socket_port': 8099})

if __name__ == '__main__':
        cherrypy.quickstart(HelloWorld())
