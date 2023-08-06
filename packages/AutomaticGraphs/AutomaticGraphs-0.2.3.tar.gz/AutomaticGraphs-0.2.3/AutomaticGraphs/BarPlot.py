# Import necessary packages
import matplotlib.pyplot as plt
import seaborn as sns
from .AutomaticGraphs import AutomaticGraphs

# Class for the bar graph
class barplot:
    '''Class for the bar graph plot

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

    def __init__(self, style, figsize, title, data, x_data, y_data, x_label, y_label):
        AutomaticGraphs.__init__(self, style, figsize, title, data, x_data, y_data, x_label, y_label)

    # Plot the graph
    def bar_plot(self, hue=None, palette=None):
        """Function that effectively plots the bar graph

           Args:
                hue: (names of variables in data or vector data, optional)
                Inputs for plotting long-form data

                palette: (palette name, list, or dict, optional)
                Colors to use for the different levels of the hue variable.
                Should be something that can be interpreted by color_palette(),
                or a dictionary mapping hue levels to matplotlib colors.

           Returns:
                The bar graph plot
		"""
        # Set chart theme
        sns.set_theme(style=self.style)

        # Instantiate the figure and set the size
        fig, axs = plt.subplots(figsize=self.figsize)

        # Set the chart title
        plt.title(self.title, fontsize=14)

        # Bar graph parameters
        sns.barplot(data=self.data, x=self.x_data, y=self.y_data,
                    ci=None, hue=hue, palette=palette)

        # Create chart axes and plot
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.show()