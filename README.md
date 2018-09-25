
# Web Page Content Extraction Tool


[ChineseVersion](#ChineseVersion)
## 1. Purpose
Used to extract text from the web page, this tool is appropriate for the web page which contains lots of text. This tool support both English and Chinese web pages.
## 2. How to use
First you need to initialize a 'cx' object:

```
from CxExtractor import CxExtractor
cx = CxExtractor(threshold=186)
```

For extracting text from a web page, You can read a HTML file from your disk:

```
html = cx.readHtml("E:\\Documents\\123.html")
```

or get the HTML from Internet:

```
html = cx.getHtml('http://news.163.com/16/0101/10/BC84MRHS00014AED.html')
```

Then you need to filter the tags in HTML and extract the text:
```
content = cx.filter_tags(html)
text = cx.getText(content)
print(text)
```

Finally, you can get the text in this HTML.
Notice:The constructor has two parameters that you may need to adjust.

> threshold: The length of lines in the web page should exceed the threshold so   that the lines could be recognized as useful. 

> blocksWidth: If the text rows in the web page are sparse, you should set blocksWidth larger, the default value is 3.

## 3. Demo
If you have a news web page like this:
![image](/img/html-en.png)

you can get the text by using this tool like this:

![image](/img/text-en.png)



_______________________________________





# <a name='ChineseVersion'>网页正文抽取工具</a>

![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)

## 1. 用途
  本工具用于抽取网页中的正文，常见的网页通常分为两种。
  第一种是类似于门户网站的首页，这种网页是导航页面，有很多的超链接和文章标题，这种网页本身并没有实质内容，因此这里不考虑这种网页。
  第二种是有实质性内容的网页，例如新闻的页面，这里实现的效果就是对网页进行处理，剔除其中的html标签、超链接、脚本代码等内容，抽取出网页的正文。
  这个方法只适用于有大段正文的中文网页，例如新闻、博客，不适用于微博、贴吧等等。
## 2. 原理
  这个工具是本人自己完成的cx_extractor的Python版本，基于行块分布函数，行块分布函数的提出基于以下三个推论：
  - HTML每一行都表示一个完整的语义。
  - 网页正文内容在网页中的位置很近。
  - 正文内容的一行中HTML代码的标签较少，超链接占总长度的比例不大。

因此，网页中符合上述三个条件的行被认为是正文所在的行。由此我们可以得出这样的结论：网页的正文区域是文字密度较大的区域。但是这个结论也有局限性，例如网页中出现的大篇幅文字导航信息，其文字密度较高但不是网页正文。如下图所示：

![image](/img/1.png)

因此，我们还需要考虑文字行块的长度，因为导航的长度较短而正文行的长度较长。在处理网页时需要先将网页中的所有HTML标签去除，保留空白行和文字，留下的文本记作content。求解行块分布函数的步骤如下：
- 行块：
以 content中的行号为轴，取其周围 K 行（K<5，这里取K=3，方向向下，K称为行块厚度），合起来称为一个行块block，行块i是以 content中行号 i 为轴的行块。
- 行块长度：
一个行块block，去掉其中的所有空白符（ \n,\r,\t 等）后的字符总数称为该行块的长度。
- 行块分布函数：
如果以content的每行为轴，那么这篇网页总共有LinesNum(content)-K个block，做出以[1, LinesNum(content)-K]为横轴，以其各自的行块长度为纵轴的分布函数。
对 http://www.gov.cn/ldhd/2009-11/08/content_1459564.htm 这个网页求出的行块分布函数曲线如下图所示，该网页的正文区域为145行至182行。

![image](/img/2.png)

由上图可知，正确的文本区域全都是分布函数图上含有最值且连续的一个区域，这个区域往往含有一个骤升点和一个骤降点。因此，网页正文抽取问题转化为了求行块分布函数上的骤升点和骤降点两个边界点，这两个边界点所含的区域包含了当前网页的行块长度最大值并且是连续的。
求出正文区域所在的起始行块号x\_start和终止行块号x\_end，x是行号，Y(x)是编号为x的行块的长度，Y(x)需要满足下列条件：
- 第一：Y(x\_start )>Y(x\_t)，x\_t是第一个骤升点，骤升点的行块长度必须超过某一个阈值。
- 第二：Y(x_n )≠0，n∈[start+1,start+K]，K是行块厚度，骤升点之后的第一个点的行块长度不能为0，避免出现误差。
- 第三：Y(x_m )=0，m∈[end,end+1]，骤降点以及其尾随的点的行块长度为0，保证正文在骤降点结束。
- 第四：存在 x∈[start,end]，使得Y(x)最大，以此保证骤升点和骤降点之间的区域中包括行块长度最大的点。

经过大量实验，证明此方法对于中文网页的正文提取有较高的准确度,此算法的优点在于，行块函数不依赖与HTML代码，与HTML标签无关，实现简单，准确率较高。




## 3. 接口及其使用方法

使用时导入cx_extractor_python类，并且新建cx_extractor_python类的对象。获取html页面的方式有两种，第一种是从url中获取网页，使用getHtml方法；第二种是从已经有的网页文件中读取网页，使用readHtml方法。读取网页之后，调用filter_tags方法对网页进行预处理，这个方法可以剔除网页中的html标签和js脚本等。网页预处理之后，调用getText方法就可以得到网页的正文。示例代码如下所示：



```
from CxExtractor import CxExtractor
cx = CxExtractor(threshold=186)
# test_html = cx.readHtml("E:\\Documents\\123.html")
test_html = cx.getHtml('http://news.163.com/16/0101/10/BC84MRHS00014AED.html')
content = cx.filter_tags(test_html)
s = cx.getText(content)
print(s)
```
## 4. 测试结果 
本人使用了74个网易新闻的页面进行测试，抽取正文的准确率达到90%以上。文件中的Rawhtml文件夹下是原始的网页文件，Text文件夹下是对应每一个原始网页抽取出的正文。（为什么用这74个网页呢，因为我做本科毕设的时候用网络爬虫抓新闻网页并且对新闻分类，下载了很多网页，因为下载的网页太多，删掉了以前抓取的网页，最后一次抓取的就是这74个网页，我也是在做毕设的时候接触到了这个网页正文抽取的算法，那时候我用的是Java版本的）
例如对如下的页面抽取正文：
![image](/img/raw.png)

得到的结果如下所示，可以看出，原始网页上的标签和js脚本都被剔除，并且可以正确的提取出新闻网页的正文。

![image](/img/text.png)


## 5. 更新
原本的Cx-extractor算法只适用于中文网页，我对算法进行了改进，现在支持从英文网页中提取文本。我用了bbc news上的175个新闻网页做测试，提取bbc news新闻文本的准确率在90%以上，测试的代码在testEnglish.py文件里。由于英文的句子中字符数量较多，因此要将threshold设置大一些，这里设置为186。bbc news新闻网页的源文件在bbcnews-html目录下，提取出的新闻文本在bbcnews-text目录下。提取的效果如图所示。

html网页：

![image](/img/html-en.png)

新闻文本：

![image](/img/text-en.png)

