from matplotlib import cycler

font_defaults = {
    "font.size": 16,
    "axes.labelsize": 20,
}
figure_defaults = {
    "figure.figsize": [
        9.0,
        4.8
    ],
}
tick_defaults = {
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 10,
    "ytick.major.size": 10,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.minor.size": 5,
    "ytick.minor.size": 5,
    "xtick.minor.width": 1.2,
    "ytick.minor.width": 1.2,
}
legend_defaults = {
    "legend.borderpad": .5,
    "legend.borderaxespad": 1.,
    "legend.edgecolor": [
        0.2,
        0.2,
        0.2
    ]
}
yagamee_rcparams = dict({}, **font_defaults, **figure_defaults, **tick_defaults, **legend_defaults)