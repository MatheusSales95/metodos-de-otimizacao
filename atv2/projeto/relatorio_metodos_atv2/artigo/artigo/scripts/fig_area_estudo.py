import math

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

DATA_DIR = 'PEmSE-20261028T191401Z-1-001/PEmSE'
SAIDA = 'artigo/figuras/area_estudo.png'

COR_AREA = '#ffd23f'
COR_PASSAGEM = '#4dd0e1'

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'mathtext.fontset': 'stix',
})

area_interesse = gpd.read_file(f'{DATA_DIR}/area_interesse.shp').to_crs(epsg=3857)
passagem_SAR = gpd.read_file(f'{DATA_DIR}/passagens_SAR.shp').to_crs(epsg=3857)

xmin, ymin, xmax, ymax = passagem_SAR.total_bounds
margem = 0.03 * (xmax - xmin)
xmin, xmax, ymin, ymax = xmin - margem, xmax + margem, ymin - margem, ymax + margem

largura = 3.5
fig, ax = plt.subplots(figsize=(largura, largura * (ymax - ymin) / (xmax - xmin)))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

passagem_SAR.boundary.plot(ax=ax, color=COR_PASSAGEM, linewidth=0.2, alpha=0.45, zorder=2)
area_interesse.plot(ax=ax, facecolor=COR_AREA, alpha=0.25, edgecolor='none', zorder=3)
area_interesse.boundary.plot(ax=ax, color=COR_AREA, linewidth=1.0, zorder=4)

ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs=area_interesse.crs, attribution=False)

lat = math.degrees(math.atan(math.sinh(((ymin + ymax) / 2) / 6378137)))
comprimento = 200e3 / math.cos(math.radians(lat))
x0, y0 = xmin + 0.04 * (xmax - xmin), ymin + 0.07 * (ymax - ymin)
ax.plot([x0, x0 + comprimento], [y0, y0], color='white', linewidth=2, solid_capstyle='butt', zorder=5)
ax.text(x0 + comprimento / 2, y0 + 0.025 * (ymax - ymin), '200 km', color='white',
        fontsize=8, ha='center', va='bottom', zorder=5)

ax.legend(
    handles=[
        Patch(facecolor=(1.0, 0.82, 0.25, 0.25), edgecolor=COR_AREA, linewidth=1.0, label='Áreas de interesse'),
        Line2D([], [], color=COR_PASSAGEM, linewidth=0.8, label='Passagens SAR ($N = 702$)'),
    ],
    loc='upper left', fontsize=8, frameon=True, framealpha=0.9, facecolor='white',
    edgecolor='none', handlelength=1.6, borderpad=0.5,
)

ax.set_axis_off()
fig.savefig(SAIDA, dpi=300, bbox_inches='tight', pad_inches=0.01)
print(f'salvo em {SAIDA}')
