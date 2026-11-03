import json
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator

DADOS = 'artigo/dados/convergencia_colab.json'
PASTA = 'artigo/figuras'
LARGURA = 3.5

BASE = '#262624'
VAR1 = '#2a78d6'
VAR2 = '#eb6834'
GRADE = '#e1e0d9'
EIXO = '#c3c2b7'
TINTA = '#0b0b0b'
TINTA2 = '#52514e'
TRACO = (0, (4, 2))

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'mathtext.fontset': 'stix',
    'font.size': 8,
    'pdf.fonttype': 42,
    'axes.edgecolor': EIXO,
    'axes.linewidth': 0.6,
    'axes.labelcolor': TINTA2,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.color': TINTA2,
    'ytick.color': TINTA2,
    'xtick.major.size': 0,
    'ytick.major.size': 0,
    'legend.labelcolor': TINTA,
    'legend.fontsize': 8,
    'legend.frameon': False,
    'legend.handlelength': 2.2,
})

d = json.load(open(DADOS, encoding='utf-8'))
geracoes = list(range(40))
previa = sys.argv[1] if len(sys.argv) > 1 else None


def linha(ax, y, cor, tracejada=False):
    ax.plot(geracoes, y, color=cor, lw=1.0 if tracejada else 1.4, ls=TRACO if tracejada else '-',
            solid_capstyle='round', solid_joinstyle='round', dash_capstyle='round')


def chave(cor, rotulo):
    return Line2D([], [], color=cor, lw=1.4, label=rotulo)


def legenda_estilo(ax, extra=()):
    estilos = [Line2D([], [], color=TINTA2, lw=1.4, label='melhor'),
               Line2D([], [], color=TINTA2, lw=1.0, ls=TRACO, label='média'), *extra]
    ax.add_artist(ax.legend(handles=estilos, loc='lower right'))


def numero(v, _):
    texto = f'{v:.1f}'.replace('.', ',')
    return '0,0' if texto in ('-0,0', '0,0') else texto.replace('-', '−')


def eixos(ax, rotulo_x=True):
    ax.set_xlim(0, 39)
    ax.set_ylim(-0.15, 0.25)
    ax.set_xticks([0, 10, 20, 30, 39])
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(FuncFormatter(numero))
    ax.grid(axis='y', color=GRADE, lw=0.5)
    ax.set_axisbelow(True)
    ax.set_ylabel('Aptidão, $f$')
    if rotulo_x:
        ax.set_xlabel('Geração')


def salva(fig, nome):
    fig.tight_layout(pad=0.3, h_pad=1.0)
    fig.savefig(f'{PASTA}/{nome}.pdf', bbox_inches='tight', pad_inches=0.02)
    if previa:
        fig.savefig(f'{previa}/{nome}.png', dpi=250, bbox_inches='tight', pad_inches=0.02)
    print(f'salvo em {PASTA}/{nome}.pdf')


fig, ax = plt.subplots(figsize=(LARGURA, 2.4))
legenda_estilo(ax)
for nome, cor in (('torneio', BASE), ('roleta', VAR1), ('ranking', VAR2)):
    linha(ax, d['selecao'][nome]['melhor'], cor)
    linha(ax, d['selecao'][nome]['media'], cor, tracejada=True)
ax.legend(handles=[chave(BASE, 'Torneio, $k$ = 3 (base)'), chave(VAR1, 'Roleta'), chave(VAR2, 'Ranking linear')],
          loc='upper left')
eixos(ax)
salva(fig, 'selecao')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(LARGURA, 4.0), sharex=True)
for nome, cor in (('pc_0.8', BASE), ('pc_0.6', VAR1), ('pc_0.9', VAR2)):
    linha(ax1, d['taxas'][nome], cor)
ax1.legend(handles=[chave(BASE, '$p_c$ = 0,8 (base)'), chave(VAR1, '$p_c$ = 0,6'), chave(VAR2, '$p_c$ = 0,9')],
           loc='upper left')
ax1.set_title('(a) Taxa de cruzamento, com $p_m$ = 0,01', loc='left', color=TINTA, pad=4)
eixos(ax1, rotulo_x=False)
for nome, cor in (('pm_0.01', BASE), ('pm_0.005', VAR1), ('pm_0.15', VAR2)):
    linha(ax2, d['taxas'][nome], cor)
ax2.legend(handles=[chave(BASE, '$p_m$ = 0,01 (base)'), chave(VAR1, '$p_m$ = 0,005'), chave(VAR2, '$p_m$ = 0,15')],
           loc='upper left')
ax2.set_title('(b) Taxa de mutação, com $p_c$ = 0,8', loc='left', color=TINTA, pad=4)
eixos(ax2)
salva(fig, 'taxas')

fig, ax = plt.subplots(figsize=(LARGURA, 2.4))
queda = Line2D([], [], color=VAR1, marker='v', ms=4, mec='white', mew=0.6, ls='none', label='queda do melhor')
legenda_estilo(ax, extra=[queda])
for nome, cor in (('com', BASE), ('sem', VAR1)):
    linha(ax, d['elitismo'][nome]['melhor'], cor)
    linha(ax, d['elitismo'][nome]['media'], cor, tracejada=True)
sem = d['elitismo']['sem']
quedas = sem['quedas_do_melhor']
ax.plot(quedas, [sem['melhor'][g] for g in quedas], color=VAR1, marker='v', ms=4, mec='white', mew=0.6,
        ls='none', zorder=4)
ax.legend(handles=[chave(BASE, 'Com elitismo (base)'), chave(VAR1, 'Sem elitismo')], loc='upper left')
eixos(ax)
salva(fig, 'elitismo')
