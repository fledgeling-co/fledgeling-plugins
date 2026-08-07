import numpy as np
from PIL import Image
import common as C

c, r = C.cand(), C.ref()
d = C.lum(c) - C.lum(r)
x0, y0, x1, y1 = 170, 140, 830, 700
v = np.clip(0.5 + d[y0:y1, x0:x1] * 2.0, 0, 1)
Image.fromarray((v * 255).astype(np.uint8)).save("resid-block-signed.png")
print("grey=agree, white=we are brighter, black=we are darker; gain 2x")
