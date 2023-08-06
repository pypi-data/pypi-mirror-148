# General root class for the leafs
class AutomaticGraphs:
    def __init__(self, style, figsize, title, data, x_data, y_data, x_label, y_label):
        '''Generic graphs class based in matplotlib and seaborn
        to plot the graphs automatically without having to write
        large blocks of code for each type of graph you are going to plot

            Attributes:
                style: (string or dict)
                Axes style parameters, see axes_style() in
                "https://seaborn.pydata.org/generated/seaborn.axes_style.html#seaborn.axes_style"

                figsize: (float, float)
                Width, height in inches of the graph

                title: (string)
                Text to use for the title

                data: (DataFrame, array, or list of arrays)
                Dataset for plotting

                x_data: (names of variables in data or vector data)
                Inputs for plotting long-form data

                y_data: (names of variables in data or vector data)
                Inputs for plotting long-form data

                x_label: (string)
                The x label text

                y_label (string)
                The y label text
        '''
        self.style = style
        self.figsize = figsize
        self.title = title
        self.data = data
        self.x_data = x_data
        self.y_data = y_data
        self.x_label = x_label
        self.y_label = y_label