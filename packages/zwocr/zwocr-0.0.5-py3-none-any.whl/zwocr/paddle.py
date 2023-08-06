from paddleocr import PaddleOCR,draw_ocr

class ZWPaddleOCR(object):
    ocrs = {}
    def __init__(self, lang, use_angle_cls=False) -> None:
        # `ch`, `en`, `fr`, `german`, `korean`, `japan`
        if lang not in ZWPaddleOCR.ocrs:
            # need to run only once to download and load model into memory
            ZWPaddleOCR.ocrs[lang] = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
        self.use_angle_cls = use_angle_cls
        self.engine = ZWPaddleOCR.ocrs[lang]

    def ocr_image(self, imgpth):
        result = self.engine.ocr(str(imgpth), cls=self.use_angle_cls)
        s = ''
        for line in result:
            s += line[1][0]
        return s
