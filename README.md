# -
团支书小助手
无聊的时候搞出来的东西，写的有点拉轻点喷有如有完善非常感谢！

前置安装：Tesseract-OCR 给个链接 https://github.com/tesseract-ocr/tesseract
安装时如果更改位置，需要修改app.py文件内
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'的路径位置以确保正常使用
安装python相应库即可运行 
使用时需要下载img的自建识别库
放入 Program Files\Tesseract-OCR\tessdata 才能使用
REQUIRED_TEXTS = ["  "] 内为需要识别截图的文字，方法为全部匹配若[]内关键词其中有一个不存在则这张上传的图片就判断为不符合
