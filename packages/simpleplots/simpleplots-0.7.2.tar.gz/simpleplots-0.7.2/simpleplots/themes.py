# -*- coding: utf-8 -*-

"""
simpleplots.themes
~~~~~~~~~~~~~~~~~~

This module contains simpleplots' figure themes.

"""

__all__ = ('StandardTheme')

from .base import Theme

#-------------------------------------------------------------------------------

class StandardTheme(Theme):
    figure_background_color = (255, 255, 255)

    spine_box_width_perc = 0.8
    spine_box_height_perc = 0.7
    spine_box_add_hor_offset = 0.2
    spine_box_add_ver_offset = 0.2
    spine_color = (0, 0, 0)
    spine_width = 4

    grid_box_width_perc = 0.9
    grid_box_height_perc = 0.9
    grid_visibility = True
    grid_line_color = (0, 0, 0)
    grid_line_width = 2

    tick_length_perc = 0.0075
    tick_line_color = (0, 0, 0)
    tick_line_width = 3

    tick_label_font = 'arial.ttf'
    tick_label_size_perc = 0.016
    tick_label_color = (0, 0, 0)

    title_font = 'arial.ttf'
    title_size_perc = 0.033
    title_color = (0, 0, 0)

    legend_font = 'arial.ttf'
    legend_size_perc = 0.02
    legend_color = (0, 0, 0)

#-------------------------------------------------------------------------------
