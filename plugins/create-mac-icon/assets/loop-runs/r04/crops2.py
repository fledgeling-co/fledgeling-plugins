from PIL import Image
D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/"
Image.open(D + "r03/candidate-1024.png").convert("RGB").crop((300, 700, 760, 840)) \
    .resize((1380, 420), Image.NEAREST).save(D + "r04/crop-front-base.png")
