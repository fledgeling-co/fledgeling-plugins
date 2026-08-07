from PIL import Image
A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/"
box = (170, 220, 510, 500)
for src, out in ((A + "icon.png", "crop-curl-after.png"),
                 (A + "loop-runs/r01/candidate-1024.png", "crop-curl-before.png"),
                 (A + "loop-runs/r01/reference-1024.png", "crop-curl-ref.png")):
    im = Image.open(src).convert("RGB").resize((1024, 1024)).crop(box)
    im.resize((im.width * 3, im.height * 3), Image.LANCZOS).save(A + "loop-runs/r04/" + out)
print("ok")
