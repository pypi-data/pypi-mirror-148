from itertools import product

from .colors import (
    BLACK,
    BLUE,
    COLOR_DICT,
    GREEN,
    GREY,
    LIGHT_BLUE,
    LIGHT_GREEN,
    LIGHT_GREY,
    LIGHT_PINK,
    LIGHT_YELLOW,
    PINK,
    WHITE,
    YELLOW,
)
from .utils import register_blended_cmap, register_listed_cmap

####################################################################################################
# DISCRETE COLORMAPS
####################################################################################################

default_colors = [
    BLUE,
    PINK,
    GREEN,
    YELLOW,
    GREY,
    LIGHT_BLUE,
    LIGHT_PINK,
    LIGHT_GREEN,
    LIGHT_YELLOW,
    LIGHT_GREY,
]
default_cmap = register_listed_cmap(default_colors, "stwx:default")

paired_colors = [
    BLUE,
    LIGHT_BLUE,
    PINK,
    LIGHT_PINK,
    GREEN,
    LIGHT_GREEN,
    YELLOW,
    LIGHT_YELLOW,
    GREY,
    LIGHT_GREY,
]
paired_cmap = register_listed_cmap(paired_colors, "stwx:paired")

deep_colors = [
    BLUE,
    PINK,
    GREEN,
    YELLOW,
    GREY,
]
deep_cmap = register_listed_cmap(deep_colors, "stwx:deep")

light_colors = [
    LIGHT_BLUE,
    LIGHT_PINK,
    LIGHT_GREEN,
    LIGHT_YELLOW,
    LIGHT_GREY,
]
light_cmap = register_listed_cmap(light_colors, "stwx:light")

black_colors = [
    BLACK,
    BLUE,
    PINK,
    GREEN,
    YELLOW,
    GREY,
    LIGHT_BLUE,
    LIGHT_PINK,
    LIGHT_GREEN,
    LIGHT_YELLOW,
    LIGHT_GREY,
]
black_cmap = register_listed_cmap(black_colors, "stwx:black")

####################################################################################################
# BLENDED COLORMAPS
####################################################################################################

bad2good_colors = [PINK, YELLOW, GREEN]
bad2good_cmap = register_blended_cmap(bad2good_colors, "stwx:bad2good")

good2bad_colors = [GREEN, YELLOW, PINK]
good2bad_cmap = register_blended_cmap(good2bad_colors, "stwx:good2bad")

for (name1, color1), (name2, color2) in product(COLOR_DICT.items(), COLOR_DICT.items()):
    cmap_colors_ = [color1, WHITE, color2]
    cmap_name_ = f"stwx:{name1}{name2}_diverging"
    _ = register_blended_cmap(cmap_colors_, cmap_name_)

for (name1, color1), (name2, color2) in product(COLOR_DICT.items(), COLOR_DICT.items()):
    if name1 != name2:
        cmap_colors_ = [color1, color2]
        cmap_name_ = f"stwx:{name1}{name2}_blend"
        _ = register_blended_cmap(cmap_colors_, cmap_name_)

for name, color in COLOR_DICT.items():
    cmap_colors_ = [color, WHITE]
    cmap_name_ = f"stwx:{name}_fade"
    _ = register_blended_cmap(cmap_colors_, cmap_name_)

for name, color in COLOR_DICT.items():
    cmap_colors_ = [BLACK, color, WHITE]
    cmap_name_ = f"stwx:{name}_rise"
    _ = register_blended_cmap(cmap_colors_, cmap_name_)
