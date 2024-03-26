from typing import Annotated
from fastapi import FastAPI, Request, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from domain.processor import Processor
import uuid
import shutil

processor = Processor()

app = FastAPI()

templates = Jinja2Templates(directory="ui/web/frontend/dist")

app.mount("/assets", StaticFiles(directory="ui/web/frontend/dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="ui/web/frontend/dist/static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.get("/_info")
def info():
    return {"status": "ok"}

@app.post("/api/process")
def info(
    request: Request,
    text: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
):
    data = processor.make_data()

    processor.set_text_and_speaker(data, text, 'en_0')

    processor.make_speech(data)

    ext = image.filename.split('.')[-1]
    image_path = 'data/'+str(uuid.uuid4())+'.'+ext
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
    processor.add_image(data, image_path)

    processor.make_video(data)

    return {"status": "ok", "speech": '/'+data.audio_file_path, "video": '/'+data.video_file_path}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )
