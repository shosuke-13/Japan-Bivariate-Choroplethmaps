import matplotlib.pyplot as plt

# Define percentile bounds for color classes
percentile_limits = [0.1, 0.3, 0.6, 1.0]

# Function to convert hex color to RGB
def hex_to_rgb_color(hex_code):
    rgb_values = [int(hex_code[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    return rgb_values

# Define corner colors
light_gray = hex_to_rgb_color('#e8e8e8')
green = hex_to_rgb_color('#73ae80')
blue = hex_to_rgb_color('#6c83b5')
dark_blue = hex_to_rgb_color('#2a5a5b')

# Create a square grid of colors using color interpolation
num_groups = len(percentile_limits)
light_gray_to_green = []
blue_to_dark_blue = []
color_list = []

for i in range(num_groups):
    light_gray_to_green.append([light_gray[j] + (green[j] - light_gray[j]) * i / (num_groups - 1) for j in range(3)])
    blue_to_dark_blue.append([blue[j] + (dark_blue[j] - blue[j]) * i / (num_groups - 1) for j in range(3)])

for i in range(num_groups):
    for j in range(num_groups):
        color_list.append([light_gray_to_green[i][k] + (blue_to_dark_blue[i][k] - light_gray_to_green[i][k]) * j / (num_groups - 1) for k in range(3)])

# Convert colors to hex
color_list_hex = ['#%02x%02x%02x' % tuple(int(c * 255) for c in color) for color in color_list]

# Function to get bivariate color given two percentiles
def get_bivariate_color(p1, p2):
    if p1 >= 0 and p2 >= 0:
        i = next(i for i, pb in enumerate(percentile_limits) if p1 <= pb)
        j = next(j for j, pb in enumerate(percentile_limits) if p2 <= pb)
        return color_list_hex[i * num_groups + j]
    else:
        return '#cccccc'  # Gray for invalid percentiles

# Other parameters
alpha_value = 0.85
dpi_value = 3000

"""Geometry dataframe represents GIS data, including geometry column and other relevant columns"""

# Plot map based on bivariate choropleth
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
geometry['color_bivariate'] = [get_bivariate_color(p1, p2) for p1, p2 in zip(geometry['column1'].values, geometry['column2'].values)]
geometry.plot(ax=ax, color=geometry['color_bivariate'], alpha=alpha_value, legend=False)
ax.set_xticks([])
ax.set_yticks([])

# Create inset legend
ax_inset = ax.inset_axes([0.6, 0.1, 0.33, 0.3])
ax_inset.set_aspect('equal', adjustable='box')
x_ticks = [0]
y_ticks = [0]

for i, percentile_bound_p1 in enumerate(percentile_limits):
    for j, percentile_bound_p2 in enumerate(percentile_limits):
        rect = plt.Rectangle((i, j), 1, 1, facecolor=color_list_hex[i * num_groups + j], alpha=alpha_value)
        ax_inset.add_patch(rect)
        if i == 0:
            y_ticks.append(percentile_bound_p2)
    x_ticks.append(percentile_bound_p1)

ax_inset.set_xlim([0, len(percentile_limits)])
ax_inset.set_ylim([0, len(percentile_limits)])
ax_inset.set_xticks(list(range(len(percentile_limits) + 1)), x_ticks)
ax_inset.set_xlabel('Distribution Percentile')
ax_inset.set_yticks(list(range(len(percentile_limits) + 1)), y_ticks)
ax_inset.set_ylabel('Distribution Percentile')

plt.show()
