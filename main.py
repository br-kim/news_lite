import requests
from bs4 import BeautifulSoup, NavigableString
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

import uvicorn

app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("main_page.html")


@app.get("/bbc")
async def bbc_news(provider, url):
    news_url = url
    res = requests.get(news_url)
    soup = BeautifulSoup(res.text, "html.parser")
    res1 = soup.find_all('main')
    main_text = res1[0].find_all(['h1', 'time', 'ul', 'h2', 'p'])
    title = main_text
    result = []
    for element in title:
        if element.find("a"):
            for content in element.descendants:
                if isinstance(content, NavigableString):
                    result.append(content)
        else:
            result.append(element)

    return HTMLResponse("".join([str(i) for i in result]))


if __name__ == "__main__":
    uvicorn.run("main:app")
