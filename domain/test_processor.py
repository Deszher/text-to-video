import os
from domain.processor import Processor


def test_make_speech():
    processor = Processor()

    data = processor.make_data()

    processor.set_text_and_speaker(data, "test", "en_0")

    processor.make_speech(data)

    assert data.audio_file_path is not None
    assert data.audio_file_path != ""
    assert os.path.exists(data.audio_file_path)
