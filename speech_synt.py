import os

import torch


def get_speech(text, selected_speaker):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v6_en.pt',
                                       local_file)

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    sample_rate = 48000

    audio_paths = model.save_wav(text=text,
                                 speaker=selected_speaker,
                                 sample_rate=sample_rate)
    print(audio_paths)

get_speech("text", "en_99")