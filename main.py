from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# 只创建 FastAPI 应用，不要 Flask！
app = FastAPI()

# 挂载静态文件夹 → 图片/CSS/JS 靠这个生效！
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板文件夹
templates = Jinja2Templates(directory="templates")

# 首页
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 歌曲页面
@app.get("/song1", response_class=HTMLResponse)
async def read_song1(request: Request):
    return templates.TemplateResponse("song1.html", {"request": request})