
class ProcessData:
    input_text: str = None
    input_speaker: str = None

    audio_file_path: str = None
    image_file_path: str = None
    video_file_path: str = None

    def audio_file_name(self) -> str:
        return self.audio_file_path.split('/')[1]