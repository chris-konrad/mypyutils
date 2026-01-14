"""
Created on Thu Dec 18 09:02:26 2025

Plotting functions

@author: Christoph M. Konrad
"""
import numpy as np
import matplotlib.pyplot as plt


def subplots_from_aspect(n_plots, aspect=1.78, **kwargs):
    """Create a grid of suplots with the given aspect ratio fitting at least n_plots. 

    Parameters
    ----------
    n_plots : int
        Number of plots. The resulting grid will fit at least this number.
    aspect : float, optional
        The ratio of columns to rows, i.e. aspect = ncols/nrows. The default is 16:9.
    kwargs : 
        Any keyword arguments of plt.subplots()

    Returns
    -------
    fig
        Matplotlib figure
    axes
        Array of axes. 
    """

    rows = np.ceil(np.sqrt(n_plots/aspect))
    cols = np.ceil(n_plots/rows)

    fig, axes = plt.subplots(int(rows), int(cols), **kwargs)

    return fig, axes
