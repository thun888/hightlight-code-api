# -*- coding:utf-8 -*-
from re import findall

import requests
import uvicorn
import json
from fastapi import FastAPI,Response
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name,get_lexer_for_filename
app = FastAPI(docs_url=None, redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=str(True),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/generate", response_class=Response)
def vOneGenerate(response: Response,code: str = "",url: str = "",lang: str = "",withcss: bool = True,usejson: bool = False,showsupporter: bool = True):
    filename = 'InputCode'
    if url != "":
        filename = url.split('/')[-1]
        code = requests.get(url).text
        # 进行转义
        code = code.replace('\\', '\\\\')
        if lang != "":
            lexer = get_lexer_by_name(lang)
        else:
            lexer = get_lexer_for_filename(filename)

    # 使用HTML formatter进行格式化
    formatter = HtmlFormatter(linenos=True)
    # 进行高亮
    result = highlight(code, lexer, formatter)
    # 添加文件名字及语言类型
    result = result.replace('<div class="highlight">', '<div class="highlight ' + lang + '"><figcaption><span>' + filename + '</span></figcaption>')
    result = result.replace('class="linenos"', 'class="linenos" style="padding: 0 1em;"')
    # 压缩成一行
    # 只去掉末尾的一个<br>
    result = result.replace('\n', '<br>')[:-4]
    if showsupporter:
        result = result + '<div class="highlightcode-meta"><a href="'+url+'" style="float:right">view raw</a><a href="'+url+'">'+filename+'</a> transformed with ❤️ by <a href="https://hzchu.top">Hzchu.top</a></div>'
    if usejson:
        # 设置Content-Type为json
        output = json.dumps({'result': result})
        response.headers['Content-Type'] = 'application/json'
        return output
    
    output = 'document.write(\''+ result + '\') '
    if withcss:
        output = output + '''\ndocument.write('<link rel="stylesheet" href="https://jsd.hzchu.top/gh/thun888/assets@master/files/pygments-css/default.css">')'''
    return output

@app.get("/", response_class=Response)
def index():
    return "Hello World"

if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", reload=True)
        # uvicorn.run("main:app", host="0.0.0.0", reload=True,port=18081)
