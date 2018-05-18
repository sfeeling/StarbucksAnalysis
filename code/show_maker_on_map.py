from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

lat = 20.5937
lon = 78.9629
points_with_annotation = list()

#Event is set for any movement and annotations are set to visible when on points with anotation
def on_move(event):
    visibility_changed = False
    for point, annotation in points_with_annotation:
        should_be_visible = (point.contains(event)[0] == True)

        if should_be_visible != annotation.get_visible():
            visibility_changed = True
            annotation.set_visible(should_be_visible)

    if visibility_changed:
        plt.draw()


fig = plt.figure()
ax = plt.axes()

m = Basemap(projection='mill', llcrnrlat=-90, llcrnrlon=-180, urcrnrlat=90, urcrnrlon=180, resolution='c')
m.fillcontinents(color='white', lake_color='white')
m.drawcoastlines(linewidth=0.5, color='k')
m.drawcountries(linewidth=0.5, color='k')
m.drawmapboundary(fill_color='white')

xpt, ypt = m(lon,lat)
point, = m.plot(xpt, ypt, marker='o', markersize=5, alpha=0.85, visible=True)
annotation = ax.annotate("Lat: %s Lon: %s" % (lat,lon),
    xy=(xpt, ypt), xycoords='data',
    xytext=(xpt + 1, ypt), textcoords='data',
    horizontalalignment="left",
    arrowprops=dict(arrowstyle="simple",
    connectionstyle="arc3,rad=-0.2"),
    bbox=dict(boxstyle="round", facecolor="w",
    edgecolor="0.5", alpha=0.9)
        )


annotation.set_visible(False)
points_with_annotation.append([point, annotation])
on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
plt.show()