from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from fastapi.templating import Jinja2Templates
from models import DBMessage
from fastapi.staticfiles import StaticFiles

# 1. 初始化应用
app = FastAPI()

# 2. 挂载静态文件夹 (CSS/Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. 模板引擎配置
templates = Jinja2Templates(directory="templates")

# 4. 确保数据库表已创建
Base.metadata.create_all(bind=engine)

# --- 路由部分 ---

# 首页：合并了之前的两个 home 函数，现在支持读取留言
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # 从数据库读取所有留言，并按时间倒序排列
    messages = db.query(DBMessage).order_by(DBMessage.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "messages": messages
    })

# 歌曲页面 [cite: 55]
@app.get("/song1", response_class=HTMLResponse)
async def read_song1(request: Request):
    return templates.TemplateResponse("song1.html", {"request": request})

# 留言提交接口 [cite: 56, 70]
@app.post("/messages/create")
async def create_message(content: str = Form(...), db: Session = Depends(get_db)):
    # 创建并保存新留言
    new_msg = DBMessage(content=content)
    db.add(new_msg)
    db.commit()
    # 提交后利用 303 状态码重定向回首页留言板位置
    return RedirectResponse(url="/#message-board", status_code=303)