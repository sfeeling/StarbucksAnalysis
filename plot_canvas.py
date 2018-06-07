import pandas as pd
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from geonamescache import GeonamesCache
import matplotlib.colors as colors

from top_k import TopK
from csv_process import DataProcess
from radius import Radius

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

stb_file = pd.read_csv('directory.csv')
dp = DataProcess()  # 读取文件
country_codes = dp.country()
lon = dp.lon() # 经度列表
lat = dp.lat()  # 纬度列表
timezone = dp.timezone()  # 时区列表
marker_label = dp.label()

class ViewOption:
    QUERY = 0
    DESTINY = 1
    TIMEZONE = 2


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, view_option=ViewOption.QUERY):
        self.fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        self.point = None

        self.top_k = TopK()
        self.index_list = []
        self.lon_list = []
        self.lat_list = []

        self.radius = Radius()

        self.view_option = view_option

        # 查询
        if self.view_option == ViewOption.QUERY:
            self.m = Basemap(ax=self.axes, projection='mill', area_thresh=10000, llcrnrlat=-65, llcrnrlon=-180, urcrnrlat=80,
                        urcrnrlon=180,
                        resolution='c')
            self.m.fillcontinents(color='#DEDEDE', lake_color='#DEDEDE', zorder=0.1)
            self.m.drawcoastlines(linewidth=0.2, color='k')
            self.m.drawcountries(linewidth=0.5, color='k')
            self.m.drawmapboundary(fill_color='#A0CFDF')

            self.annot = self.axes.annotate("", xy=(0, 0), xytext=(-50, 20), textcoords="offset points",
                                       bbox=dict(boxstyle="round", fc="w"),
                                       arrowprops=dict(arrowstyle="->"))
            self.annot.set_visible(False)

            def update_annot(ind):
                index = self.index_list[ind["ind"][0]]
                pos = self.point.get_offsets()[ind["ind"][0]]
                self.annot.xy = pos
                # text = pd.DataFrame(stb_file.loc[index])  # 返回的文本需要做一个索引的映射
                text = marker_label[index]
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.8)

            def hover(event):
                if event.inaxes == self.axes and self.point is not None:
                    cont, ind = self.point.contains(event)
                    if cont:
                        update_annot(ind)
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                    else:
                        vis = self.annot.get_visible()
                        if vis:
                            self.annot.set_visible(False)
                            self.fig.canvas.draw_idle()

            self.fig.canvas.mpl_connect("motion_notify_event", hover)

            self.axes.set_title('店铺查询')
            self.axes.title.set_y(1.05)

        # 时区
        if self.view_option == ViewOption.TIMEZONE:
            self.m = Basemap(ax=self.axes, projection='mill', area_thresh=10000, llcrnrlat=-65, llcrnrlon=-180, urcrnrlat=80,
                        urcrnrlon=180,
                        resolution='c')
            self.m.fillcontinents(color='#DEDEDE', lake_color='#DEDEDE', zorder=0.1)
            self.m.drawcoastlines(linewidth=0.2, color='k')
            self.m.drawcountries(linewidth=0.5, color='k')
            self.m.drawmapboundary(fill_color='#A0CFDF')

            zone_dict = {}
            color_ind = 0  # cnames里的索引
            label = list()

            xpt, ypt = self.m(lon, lat)  # 把经纬度转换为x, y坐标，因为图像输出需要用到坐标


            for item in timezone:
                tz = item.split()[0]
                if not zone_dict.__contains__(tz):
                    zone_dict[tz] = 1
                else:
                    zone_dict[tz] += 1

            for item in timezone:
                tz = item.split()[0]
                count = zone_dict[tz]
                # label对应colormap的索引
                if count < 1500:
                    label.append(0)
                elif count < 3000:
                    label.append(1)
                elif count < 4500:
                    label.append(2)
                else:
                    label.append(3)

            def colormap():
                return mpl.colors.LinearSegmentedColormap.from_list('cmap',
                                                                    ['#FB7C5C', '#F6563E', '#E42F28',
                                                                     '#C3161A'], 256)

            self.point = self.m.scatter(xpt, ypt, marker='o', s=3, c=label, cmap=colormap(), zorder=1)
            self.point.set_visible(True)

            self.annot = self.axes.annotate("", xy=(0, 0), xytext=(-50, 20), textcoords="offset points",
                                       bbox=dict(boxstyle="round", fc="w"),
                                       arrowprops=dict(arrowstyle="->"))
            self.annot.set_visible(False)

            def update_annot(ind):
                index = ind['ind'][0]
                pos = self.point.get_offsets()[ind["ind"][0]]
                self.annot.xy = pos
                text = marker_label[index]
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.8)

            def hover(event):
                vis = self.annot.get_visible()
                if event.inaxes == self.axes:
                    cont, ind = self.point.contains(event)
                    if cont:
                        update_annot(ind)
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                    else:
                        if vis:
                            self.annot.set_visible(False)
                            self.fig.canvas.draw_idle()

            self.fig.canvas.mpl_connect("motion_notify_event", hover)

            bounds = [0, 1500, 3000, 4500, 6000]
            norm = mpl.colors.BoundaryNorm(bounds, colormap().N)

            ax_cbar = self.fig.add_axes([0.3, 0.17, 0.4, 0.02])
            cbar = mpl.colorbar.ColorbarBase(ax_cbar, cmap=colormap(), norm=norm, spacing='uniform', ticks=bounds,
                                             boundaries=bounds, orientation='horizontal')
            cbar.outline.set_linewidth(0.2)
            cbar.ax.tick_params(labelsize=8, labelcolor='#666666')
            self.axes.set_title('时区分布')
            self.axes.title.set_y(1.05)

        # 密度
        if self.view_option == ViewOption.DESTINY:
            gnc = GeonamesCache()
            countries = gnc.get_countries()

            counts = stb_file['Country'].value_counts()
            country_dict = {}
            for k, v in counts.iteritems():
                # print(k, round(v/countries[k]['areakm2']*1000000))
                country_dict[countries[k]['iso3']] = round(v / countries[k]['areakm2'] * 1000000)

            self.m = Basemap(ax=self.axes, projection='mill', llcrnrlat=-65, llcrnrlon=-180, urcrnrlat=80, urcrnrlon=180,
                        resolution='c')
            self.m.fillcontinents(color='#DEDEDE', lake_color='#DEDEDE', zorder=0)
            # m.drawcoastlines(linewidth=0.2, color='k')
            self.m.drawcountries(linewidth=0.5, color='k')
            self.m.drawmapboundary(fill_color='#A0CFDF')

            shapefile = 'ne_110m_admin_0_countries/ne_110m_admin_0_countries'

            # setup color bar
            color_num = 5
            cmap = mpl.cm.get_cmap('Reds')
            color_range = [cmap(i / (color_num + 1)) for i in range(color_num + 1)]
            bounds = [0, 10, 100, 1000, 10000, 100000]
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

            def colormap():
                return mpl.colors.LinearSegmentedColormap.from_list('cmap',
                                                                    ['#FBA083', '#FB7C5C', '#F6563E', '#E42F28',
                                                                     '#C3161A'], 256)

            # Read shapefile
            self.m.readshapefile(shapefile, 'units', color='#DDDDDD', linewidth=0.1)

            # Add patches
            for info, shape in zip(self.m.units_info, self.m.units):
                code = info['ADM0_A3']
                if not country_dict.__contains__(code):
                    color = '#DDDDDD'
                else:
                    if code == 'CHN' or code == 'TWN':
                        color = '#F6563E'
                    elif country_dict[code] < 10:
                        color = '#FBA083'
                    elif country_dict[code] < 100:
                        color = '#FB7C5C'
                    elif country_dict[code] < 1000:
                        color = '#F6563E'
                    elif country_dict[code] < 10000:
                        color = '#E42F28'
                    else:
                        color = '#C3161A'
                patches = [Polygon(np.array(shape), True)]
                pc = PatchCollection(patches, facecolor=color, edgecolor='None', linewidth=0)
                self.axes.add_collection(pc)

            ax_cbar = self.fig.add_axes([0.3, 0.15, 0.4, 0.02])
            cbar = mpl.colorbar.ColorbarBase(ax_cbar, cmap=colormap(), norm=norm, spacing='uniform', ticks=bounds,
                                             boundaries=bounds, orientation='horizontal')
            cbar.outline.set_linewidth(0.2)
            cbar.ax.tick_params(labelsize=8, labelcolor='#666666')

            self.axes.set_title('密度分布')

    def get_view_option(self):
        return self.view_option

    def get_fig(self):
        return self.fig

    def get_axes(self):
        return self.axes

    def get_point(self):
        return self.point

    def refresh(self):
        self.fig.canvas.draw_idle()

    def show_top_k(self, klon, klat, k, word):
        self.index_list.clear()
        self.lon_list.clear()
        self.lat_list.clear()

        self.top_k.set_values(klon, klat, k, word)
        self.index_list = self.top_k.index_list()
        self.lon_list = self.top_k.top_lon_list()
        self.lat_list = self.top_k.top_lat_list()

        xpt, ypt = self.m(self.lon_list, self.lat_list)  # 把经纬度转换为x, y坐标，因为图像输出需要用到坐标
        self.point = None
        self.point = self.m.scatter(xpt, ypt, marker='o', s=3, color='#1F77B4')

    def show_radius(self, rlon, rlat, radius):
        self.index_list.clear()
        self.lon_list.clear()
        self.lat_list.clear()

        self.radius.set_values(rlon, rlat, radius)
        self.index_list = self.radius.index_list()
        self.lon_list = self.radius.radius_lon_list()
        self.lat_list = self.radius.radius_lat_list()

        xpt, ypt = self.m(self.lon_list, self.lat_list)
        self.point = None
        self.point = self.m.scatter(xpt, ypt, marker='o', s=3, color='#1F77B4')
