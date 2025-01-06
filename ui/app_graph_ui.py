import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AppGraphUI:
    """A class to design and display graphs using Matplotlib within a Tkinter panel."""

    def __init__(self, main_panel: tk.Frame):
        """
        Initializes the graph form and embeds two subplots into the given panel.
        
        Args:
            main_panel (tk.Frame): The Tkinter frame where the graphs will be displayed.
        """
        # Create a figure with two subplots
        figure = Figure(figsize=(8, 6), dpi=100)
        ax1 = figure.add_subplot(211)
        ax2 = figure.add_subplot(212)

        # Adjust layout to provide space between subplots
        figure.subplots_adjust(hspace=0.4)

        # Generate the graphs
        self.create_bar_chart(ax1)
        self.create_line_chart(ax2)

        # Embed the figure into the Tkinter panel
        canvas = FigureCanvasTkAgg(figure, master=main_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_bar_chart(self, ax):
        """
        Creates a bar chart on the given axis.
        
        Args:
            ax: The axis where the bar chart will be plotted.
        """
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        # Create a bar chart
        ax.bar(x, y, label='Bar Chart', color='blue', alpha=0.7)

        # Customize the chart
        ax.set_title('Bar Chart Example')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.legend()

        # Add labels to each bar
        for i, v in enumerate(y):
            ax.text(x[i] - 0.1, v + 0.1, str(v), color='black')

        # Add grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    def create_line_chart(self, ax):
        """
        Creates a line chart on the given axis.
        
        Args:
            ax: The axis where the line chart will be plotted.
        """
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 1, 2, 1]

        # Create a line chart
        ax.plot(x, y, label='Line Chart', color='red', linestyle='--', marker='o')

        # Add annotations
        ax.annotate(
            'Important Point',
            xy=(3, 1),
            xytext=(3.5, 1.5),
            arrowprops=dict(facecolor='black', shrink=0.05),
        )

        # Customize the chart
        ax.set_title('Line Chart Example')
        ax.set_xlabel('X Axis', fontsize=12)
        ax.set_ylabel('Y Axis', fontsize=12)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 3)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
