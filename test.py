from CxExtractor import CxExtractor
cx = CxExtractor(threshold=186)
# html = cx.getHtml("http://www.bbc.com/news/world-europe-40885324")
# "http://news.163.com/17/0810/09/CRFF02Q100018AOR.html"
# html_url = "https://www.chunyuyisheng.com/pc/article/129283/"
# html_url = "https://dxy.com/column/3137"
# html_url = "http://news.medlive.cn/endocr/info-progress/show-149252_46.html"
html_url = "https://news.fh21.com.cn/ylzx/bjfzbdfyy/5380927.html"
html = cx.getHtml(html_url)
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
