import matplotlib.pyplot as plt

class BivariateChoroplethPlotter:
    """Bivariate choropleth plotter"""
    def __init__(self, percentile_limits):
        self.percentile_limits = percentile_limits
        self.num_groups = len(percentile_limits)
        self.alpha_value = 0.85

        self.light_gray, self.green, self.blue, self.dark_blue = self.define_corner_colors()
        self.color_list_hex = self.create_color_list()


    def hex_to_rgb_color(self, hex_code):
        rgb_values = [int(hex_code[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
        return rgb_values


    def define_corner_colors(self):
        light_gray = self.hex_to_rgb_color('#e8e8e8')
        green = self.hex_to_rgb_color('#73ae80')
        blue = self.hex_to_rgb_color('#6c83b5')
        dark_blue = self.hex_to_rgb_color('#2a5a5b')
        return light_gray, green, blue, dark_blue


    def create_color_list(self):
        light_gray_to_green = []
        blue_to_dark_blue = []
        color_list = []

        for i in range(self.num_groups):
            light_gray_to_green.append([self.light_gray[j] + (self.green[j] - self.light_gray[j]) * i / (self.num_groups - 1) for j in range(3)])
            blue_to_dark_blue.append([self.blue[j] + (self.dark_blue[j] - self.blue[j]) * i / (self.num_groups - 1) for j in range(3)])

        for i in range(self.num_groups):
            for j in range(self.num_groups):
                color_list.append([light_gray_to_green[i][k] + (blue_to_dark_blue[i][k] - light_gray_to_green[i][k]) * j / (self.num_groups - 1) for k in range(3)])

        color_list_hex = ['#%02x%02x%02x' % tuple(int(c * 255) for c in color) for color in color_list]
        return color_list_hex


    def get_bivariate_color(self, p1, p2):
        if p1 >= 0 and p2 >= 0:
            i = next(i for i, pb in enumerate(self.percentile_limits) if p1 <= pb)
            j = next(j for j, pb in enumerate(self.percentile_limits) if p2 <= pb)
            return self.color_list_hex[i * self.num_groups + j]
        else:
            return '#cccccc'  # Gray for invalid percentiles


    def plot_bivariate_choropleth(self, geometry):
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        geometry['color_bivariate'] = [self.get_bivariate_color(p1, p2) for p1, p2 in zip(geometry['column1'].values, geometry['column2'].values)]
        geometry.plot(ax=ax, color=geometry['color_bivariate'], alpha=self.alpha_value, legend=False)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()


    def plot_inset_legend(self, ax):
        ax_inset = ax.inset_axes([0.6, 0.1, 0.33, 0.3])
        ax_inset.set_aspect('equal', adjustable='box')
        x_ticks = [0]
        y_ticks = [0]

        for i, percentile_bound_p1 in enumerate(self.percentile_limits):
            for j, percentile_bound_p2 in enumerate(self.percentile_limits):
                rect = plt.Rectangle((i, j), 1, 1, facecolor=self.color_list_hex[i * self.num_groups + j], alpha=self.alpha_value)
                ax_inset.add_patch(rect)
                if i == 0:
                    y_ticks.append(percentile_bound_p2)
            x_ticks.append(percentile_bound_p1)

        ax_inset.set_xlim([0, len(self.percentile_limits)])
        ax_inset.set_ylim([0, len(self.percentile_limits)])
        ax_inset.set_xticks(list(range(len(self.percentile_limits) + 1)), x_ticks)
        ax_inset.set_xlabel('Distribution Percentile')
        ax_inset.set_yticks(list(range(len(self.percentile_limits) + 1)), y_ticks)
        ax_inset.set_ylabel('Distribution Percentile')
        plt.show()


def main():
    # Define percentile bounds for color classes
    percentile_limits = [0.1, 0.3, 0.6, 1.0]
    plotter = BivariateChoroplethPlotter(percentile_limits)

    """
    Geometry dataframe represents GIS data, including geometry column and other relevant columns

    The format of the data frame is as follows:
    geometry<pandas.dataframe or geopandas>
    | geometry | column1 | column2 |
    |----------|---------|---------|
    | Polygon  | 0.1     | 0.2     |
    | Polygon  | 0.3     | 0.4     |
    | Polygon  | 0.5     | 0.6     |
        …        …         …
    | Polygon  | 0.7     | 0.8     |
    | Polygon  | 0.9     | 1.0     |

    ※This sample uses polygon data from the national spatial data information.
    ※The data is dummy data
    """

    # Plot bivariate choropleth
    plotter.plot_bivariate_choropleth(geometry)

    # Plot inset legend
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    plotter.plot_inset_legend(ax)


if __name__ == '__main__':
    main()
