import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def plot_temperature_distribution(df):
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Extraire les températures pour chaque mois
    month_temps = [df[df['month'] == month]['température'].dropna().values for month in month_names]

    min_temp = df['température'].min()
    max_temp = df['température'].max()
    xs = np.linspace(min_temp - 3, max_temp + 3, 200)
    month_kde = [gaussian_kde(temps_i, bw_method=0.2) for temps_i in month_temps]
    max_kde = max([kde_i(xs).max() for kde_i in month_kde])
    overlap_factor = 1.9

    fig, ax = plt.subplots(figsize=(12, 8))
    for index in range(len(month_names)):
        kde = month_kde[::-1][index](xs) / max_kde * overlap_factor
        ax.plot(xs, index + kde, lw=2, color='black', zorder=50 - 2 * index + 1)
        fill_poly = ax.fill_between(xs, index, index + kde, color='none', alpha=0.8)

        verts = np.vstack([p.vertices for p in fill_poly.get_paths()])
        gradient = ax.imshow(np.linspace(min_temp, max_temp, 256).reshape(1, -1), cmap='magma', aspect='auto', zorder=50 - 2 * index,
                             extent=[verts[:, 0].min(), verts[:, 0].max(), verts[:, 1].min(), verts[:, 1].max()])
        gradient.set_clip_path(fill_poly.get_paths()[0], transform=plt.gca().transData)

    ax.set_xlim(xs[0], xs[-1])
    ax.set_ylim(ymin=-0.2)
    ax.set_xlabel('Température')
    ax.set_yticks(np.arange(len(month_names)))
    ax.set_yticklabels(month_names[::-1])
    for spine in ('top', 'left', 'right'):
        ax.spines[spine].set(visible=False)
    
    cbar = plt.colorbar(gradient, ax=ax, orientation='vertical')
    cbar.set_label('Température', rotation=270, labelpad=15)
    
    plt.tight_layout()
    plt.show()