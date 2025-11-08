import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bars(df, x, y, x_label, y_label, title, figsize, rotation):
    plt.figure(figsize=figsize)
    bars = plt.bar(df[x], df[y], color = '#0073cf')
    for bar, value in zip(bars, df[y]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + bar.get_height() * 0.01,
            str(value),
            va='bottom', ha='center', fontsize=12
        )
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(df[x],  fontsize=12, rotation=rotation)
    plt.yticks(fontsize=12)
    plt.title(title, fontsize=16, color='#ae0c00')
    plt.tight_layout()
    plt.show()

def plot_bars_horizontal(df, x, y, x_label, y_label, title, figsize):
    plt.figure(figsize=figsize)
    bars = plt.barh(df[x], df[y], color='#0073cf')
    
    for bar, value in zip(bars, df[y]):
        plt.text(
                bar.get_width() + df[y].max() * 0.005,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.0f}",
                va='center',
                ha='left',
                fontsize=12
            )

    plt.ylabel(x_label, fontsize=12)
    plt.xlabel(y_label, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.title(title, fontsize=16, color='#ae0c00')
    
    ax = plt.gca()
    ax.set_xlim(0, df[y].max() * 1.1)
    
    plt.tight_layout()
    plt.show()

def plot_line(df, x, y, title, x_label, y_label, figsize):
    plt.figure(figsize=figsize)
    sns.lineplot(data=df, x=x, y=y, marker='o', linewidth=2)
    plt.title(title, fontsize=16, color='#ae0c00')
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.show()
