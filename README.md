## Xml2Html

使用Python将XML文件转换为HTML文件
主要使用目的：工作项目中需要编写googleTest测试用例，googleTest测试用例需要使用XML格式，但是XML格式不方便查看，因此编写此工具将XML文件转换为HTML文件，方便查看。

使用场景：
1、可以融合到项目里，比如：自动编译、编译完成，自动选择对应测试用例，然后输出xml测试报告，再调用此工程，将xml转换为html，方便查看。
2、可以单独使用，比如：将原始的xml转换为html，方便查看。

### Installation
```bash
pip3 install xml2html
```
### Usage

```bash
xml2html -f <xml file path> -o <output html file>
```

### Output

![image](/assets/screenshot1.png)
