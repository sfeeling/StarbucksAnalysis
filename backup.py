# 时区
if 0:
    fig = plt.figure()
    ax = plt.axes()

    m = Basemap(projection='mill', llcrnrlat=-65, llcrnrlon=-180, urcrnrlat=75, urcrnrlon=180, resolution='c')
    m.fillcontinents(color='#DEDEDE', lake_color='#DEDEDE', zorder=0.1)
    m.drawcoastlines(linewidth=0.5, color='k')
    m.drawcountries(linewidth=0.5, color='k')
    m.drawmapboundary(fill_color='#A0CFDF')

    zone_dict = {}
    color_ind = 0  # cnames里的索引
    color_list = list(colors.cnames.values())
    label = list()

    xpt, ypt = m(lon, lat)  # 把经纬度转换为x, y坐标，因为图像输出需要用到坐标

    i = 0
    while i < len(timezone):
        item = timezone[i].split()[0]
        if not zone_dict.__contains__(item):
            zone_dict[item] = color_ind
            color_ind += 1
        label.append(zone_dict[item])
        i += 1
    print(len(zone_dict))

    point = m.scatter(xpt, ypt, marker='o', s=3, c=label, cmap=plt.cm.jet, alpha=0.5)

    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


    def update_annot(ind):

        pos = point.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = pd.DataFrame(stb_file.loc[ind["ind"][0]])
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.8)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = point.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()


    fig.canvas.mpl_connect("motion_notify_event", hover)
    ax.set_title('时区分布')



# 密度
if 0:
    gnc = GeonamesCache()
    countries = gnc.get_countries()

    counts = stb_file['Country'].value_counts()
    country_dict = {}
    for k, v in counts.iteritems():
        # print(k, round(v/countries[k]['areakm2']*1000000))
        country_dict[countries[k]['iso3']] = round(v / countries[k]['areakm2'] * 1000000)

    fig, ax = plt.subplots()

    m = Basemap(projection='mill', llcrnrlat=-70, llcrnrlon=-180, urcrnrlat=85, urcrnrlon=180, resolution='c')
    m.fillcontinents(color='#DEDEDE', lake_color='#DEDEDE', zorder=0)
    #m.drawcoastlines(linewidth=0.5, color='k')
    m.drawcountries(linewidth=0.5, color='k')
    m.drawmapboundary(fill_color='#A0CFDF')

    shapefile = 'ne_110m_admin_0_countries/ne_110m_admin_0_countries'


    # setup color bar
    color_num = 5
    cmap = mpl.cm.get_cmap('Reds')
    print(cmap)
    color_range = [cmap(i / (color_num + 1)) for i in range(color_num + 1)]
    bounds = [0, 10, 100, 1000, 10000, 100000]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


    def colormap():
        return mpl.colors.LinearSegmentedColormap.from_list('cmap',
                ['#FBA083', '#FB7C5C', '#F6563E', '#E42F28', '#C3161A'], 256)


    # Read shapefile
    m.readshapefile(shapefile, 'units', color='#DDDDDD', linewidth=0.1)

    # Add patches
    for info, shape in zip(m.units_info, m.units):
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
                print(code)
        patches = [Polygon(np.array(shape), True)]
        pc = PatchCollection(patches, facecolor=color, edgecolor='None', linewidth=0)
        ax.add_collection(pc)

    # Draw colorbar
    ax_cbar = fig.add_axes([0.3, 0.15, 0.4, 0.02])
    cbar = mpl.colorbar.ColorbarBase(ax_cbar, cmap=colormap(), norm=norm, spacing='uniform', ticks=bounds,
                                     boundaries=bounds, orientation='horizontal')
    cbar.outline.set_linewidth(0.2)
    cbar.ax.tick_params(labelsize=8, labelcolor='#666666')

    ax.set_title('密度分布')


##plt.show()