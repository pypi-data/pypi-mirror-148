import office  # 导入python-office


def test_word():
    path = '.'  # path这里，填写你存放word文件的位置，例如：C:/app/workbook
    office.word.docx2pdf(path=path)  # 程序就可以自动将该目录下的所有word文档，自动转换成pdf文档了


def test_pdf():
    office.pdf.add_watermark()


def test_wordcloud():
    office.image.txt2wordcloud('yes-minister.txt')


test_wordcloud()
