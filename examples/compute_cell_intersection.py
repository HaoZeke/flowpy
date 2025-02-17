import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt

lobe = fpy.flowpycpp.Lobe()
lobe.semi_axes = [8, 2]
lobe.thickness = 20.0
lobe.set_azimuthal_angle(np.pi / 4)
lobe.center = [20, 10]

def add_lobe(lobe, topography):
    height_data = np.zeros_like(topography.height_data)
    cells_intersect, cells_enclosed = topography.get_cells_intersecting_lobe(lobe)
    for c in cells_intersect:
        height_data[c[0], c[1]] += 1
    for c in cells_enclosed:
        height_data[c[0], c[1]] += 2
    return height_data

extent = lobe.extent_xy()

perimeter = np.array(lobe.rasterize_perimeter(30))

x_data = np.linspace(0, 40, 40)
y_data = np.linspace(0, 20, 20)
height_data = np.zeros(shape=(len(x_data), len(y_data)))

height_data = np.array(
    [[0 for j in range(len(y_data))] for i in range(len(x_data))]
)

topography = fpy.flowpycpp.Topography(height_data, x_data, y_data)

bbox = topography.bounding_box(lobe.center, extent[0], extent[1])

# "add" the lobe
new_heights = add_lobe(lobe, topography)

# Plot
cell = topography.cell_size()
plt.pcolormesh(x_data+0.5*cell, y_data+0.5*cell, new_heights.T)
plt.axvline(x_data[bbox.idx_x_lower], color="black")
plt.axvline(x_data[bbox.idx_x_higher], color="black")
plt.axhline(y_data[bbox.idx_y_lower], color="black")
plt.axhline(y_data[bbox.idx_y_higher], color="black")
plt.plot(perimeter[:, 0], perimeter[:, 1], color="white")

plt.show()