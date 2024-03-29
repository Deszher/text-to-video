import os
import uuid
import torch


def get_speech(text, selected_speaker) -> str:
    """
    return audio file path
    """
    device = torch.device("cpu")
    torch.set_num_threads(4)

    local_file = "model.pt"

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(
            "https://models.silero.ai/models/tts/en/v6_en.pt", local_file
        )

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    sample_rate = 48000

    audio_path = "data/" + str(uuid.uuid4()) + ".wav"

    audio_paths = model.save_wav(
        text=text,
        speaker=selected_speaker,
        sample_rate=sample_rate,
        audio_path=audio_path,
    )
    _ = audio_paths
    # print(audio_paths)

    return audio_path


# get_speech("text", "en_99")
