"""Processor is a facade to process logic"""
import os
import shutil
import uuid
from pathlib import Path

from domain.model import ProcessData
from domain.speech_synt import get_speech

FALLBACK_IMAGE = "ui/native_app/img/fallback_image.png"


class Processor:
    def make_data(self) -> ProcessData:
        return ProcessData()

    def set_text_and_speaker(self, data: ProcessData, text: str, speaker: str):
        if text == "":
            text = "can't say anything, you forgot to write down the text"
        data.input_text = text
        data.input_speaker = speaker
        print(data.input_text, data.input_speaker)

    def make_speech(self, data: ProcessData):
        data.audio_file_path = get_speech(data.input_text, data.input_speaker)
        print("audio path: "+data.audio_file_path)

    def add_image(self, data: ProcessData, file: str):
        ext = file.split('.')[-1]
        image_path = 'data/'+str(uuid.uuid4())+'.'+ext
        path = Path(file)

        shutil.copyfile(path, image_path)

        data.image_file_path = image_path
        print("Картинка успешно сохранена как", image_path)

    def get_image_preview(self, data: ProcessData) -> str:
        if data.image_file_path:
            return data.image_file_path
        return FALLBACK_IMAGE

    def make_video(self, data: ProcessData):
        # TODO: using data.audio_file_path and data.image_file_path make video and save to data.video_file_path
        pass

    def save_to(self, data: ProcessData, save_dir: str) -> str:
        # Путь и название сохраняемого файла
        save_path = os.path.join(save_dir, data.audio_file_name())

        # Код для сохранения файла
        shutil.copyfile(data.audio_file_path, save_path)

        print(f"Файл успешно сохранен по пути: {save_path}")

        return save_path