from genalog.degrader import Degrader
from matplotlib import pyplot as plt

# We are applying degradation effects to the images in the following sequence:
# blur -> bleed_through -> salt
degradations = [
    ("blur", {"radius": 3}),
    ("bleed_through", {"alpha": 0.8}),
    ("salt", {"amount": 0.5}),
]
# All of the referenced degradation effects are in submodule `genalog.degradation.effect`

degrader = Degrader(degradations)
dst = degrader.apply_effects(src)
plt.imshow(dst, cmap="gray")