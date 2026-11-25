"""Shared matplotlib style for pySWAP's example plots."""

# Large fonts and lines for wide figures; the same values as seaborn's
# "poster" plotting context, which these plots used before. Applied with
# matplotlib.pyplot.rc_context, so global settings are left untouched.
POSTER = {
    "axes.linewidth": 2.5,
    "grid.linewidth": 2,
    "lines.linewidth": 3.0,
    "lines.markersize": 12,
    "patch.linewidth": 2,
    "xtick.major.width": 2.5,
    "ytick.major.width": 2.5,
    "xtick.minor.width": 2,
    "ytick.minor.width": 2,
    "xtick.major.size": 12,
    "ytick.major.size": 12,
    "xtick.minor.size": 8,
    "ytick.minor.size": 8,
    "font.size": 24,
    "axes.labelsize": 24,
    "axes.titlesize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "legend.fontsize": 22,
    "legend.title_fontsize": 24,
}
