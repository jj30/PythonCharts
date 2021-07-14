import matplotlib.pyplot as plt
import cherrypy
import io
import numpy as np

category_names = ['Strongly disagree', 'Disagree',
                  'Neither agree nor disagree', 'Agree', 'Strongly agree']
results = {
    'Question 1': [10, 15, 17, 32, 26],
    'Question 2': [26, 22, 29, 10, 13],
    'Question 3': [35, 37, 7, 2, 19],
    'Question 4': [32, 11, 9, 15, 33],
    'Question 5': [21, 29, 5, 5, 40],
    'Question 6': [8, 19, 5, 30, 38]
}


# https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py
class HelloWorld(object):
        @cherrypy.expose
        def index(self):
                return ''' <img src="image.png" width="1100" height="480" border="0" /> '''

        @cherrypy.expose
        def image_png(self):
                img = io.BytesIO()
                self.plot(img)
                img.seek(0)
                return cherrypy.lib.static.serve_fileobj(img, content_type="png", name="image.png")


        def plot(self, image):
                labels = list(results.keys())
                data = np.array(list(results.values()))
                data_cum = data.cumsum(axis=1)
                category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

                fig, ax = plt.subplots(figsize=(9.2, 5))
                ax.invert_yaxis()
                ax.xaxis.set_visible(False)
                ax.set_xlim(0, np.sum(data, axis=1).max())

                for i, (colname, color) in enumerate(zip(category_names, category_colors)):
                    widths = data[:, i]
                    starts = data_cum[:, i] - widths
                    rects = ax.barh(labels, widths, left=starts, height=0.5,
                                    label=colname, color=color)

                    r, g, b, _ = color
                    text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
                    ax.bar_label(rects, label_type='center', color=text_color)
                ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                          loc='lower left', fontsize='small')

                # return fig, ax
                plt.savefig(image, format='png')

cherrypy.config.update({'server.socket_port': 8099})

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
