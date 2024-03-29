import os
import subprocess
import torchaudio

# PHONEME_JK = '[.w[]|{word: (.t | ascii_upcase | sub("<S>"; "sil") | sub("<SIL>"; "sil") | sub("\(2\)"; "") | sub("\(3\)"; "") | sub("\(4\)"; "") | sub("\[SPEECH\]"; "SIL") | sub("\[NOISE\]"; "SIL")), phones: [.w[]|{ph: .t | sub("\+SPN\+"; "SIL") | sub("\+NSN\+"; "SIL"), bg: (.b*100)|floor, ed: (.b*100+.d*100)|floor}]}]'
# PHONEME_JK = '[.w[]|{word: (.t | ascii_upcase | sub("<S>"; "sil") | sub("<SIL>"; "sil") | sub("\\(2\\)"; "") | sub("\\(3\\)"; "") | sub("\\(4\\)"; "") | sub("\\[SPEECH\\]"; "SIL") | sub("\\[NOISE\\]"; "SIL")), phones: [.w[]|{ph: .t | sub("\\+SPN\\+"; "SIL") | sub("\\+NSN\\+"; "SIL"), bg: (.b*100)|floor, ed: (.b*100+.d*100)|floor}]}]'
PHONEME_JK = '[.w[]|{word: (.t | ascii_upcase | sub("<S>"; "sil") | sub("<SIL>"; "sil") | sub("\\\\(2\\\\)"; "") | sub("\\\\(3\\\\)"; "") | sub("\\\\(4\\\\)"; "") | sub("\\\\[SPEECH\\\\]"; "SIL") | sub("\\\\[NOISE\\\\]"; "SIL")), phones: [.w[]|{ph: .t | sub("\\\\+SPN\\\\+"; "SIL") | sub("\\\\+NSN\\\\+"; "SIL"), bg: (.b*100)|floor, ed: (.b*100+.d*100)|floor}]}]'
# pocketsphinx -phone_align yes single /content/audio.wav "Can you give me cup of tea please" \
# | jq '[.w[]|{word: (.t | ascii_upcase | sub("<S>"; "sil") | sub("<SIL>"; "sil") | sub("\\(2\\)"; "") | sub("\\(3\\)"; "") | sub("\\(4\\)"; "") | sub("\\[SPEECH\\]"; "SIL") | sub("\\[NOISE\\]"; "SIL")), phones: [.w[]|{ph: .t | sub("\\+SPN\\+"; "SIL") | sub("\\+NSN\\+"; "SIL"), bg: (.b*100)|floor, ed: (.b*100+.d*100)|floor}]}]' > /content/test.json


def convert_audio_to_16k(input_path: str) -> str:
    output_path = input_path[:-4] + "_16k.wav"

    waveform, sample_rate = torchaudio.load(input_path, backend="sox")
    torchaudio.save(output_path, waveform, 16000, encoding="PCM_S", bits_per_sample=16)

    return output_path


def create_phoneme(audio_path: str, text: str) -> str:
    output_path = audio_path[:-4] + "_phoneme.json"

    response = subprocess.run(
        "pocketsphinx -phone_align yes single /app/"
        + audio_path
        + " | jq '"
        + PHONEME_JK
        + "' > /app/"
        + output_path,
        capture_output=True,
        shell=True,
        cwd="/app",
        executable="/bin/bash",
    )

    print(
        "create phoneme code, output_path: ",
        output_path,
        ", stdout:",
        response.stdout,
        "stderr:",
        response.stderr,
    )

    return output_path


def make_video(img_path: str, audio_path, phoneme_path: str) -> str:
    response = subprocess.run(
        "python test_script.py --img_path /app/"
        + img_path
        + " --audio_path /app/"
        + audio_path
        + " --phoneme_path /app/"
        + phoneme_path
        + " --save_dir /app/data",
        capture_output=True,
        shell=True,
        cwd="/app/one_shot_talking_face",
        executable="/bin/bash",
    )

    output_path = (
        "data/"
        + os.path.basename(img_path)[:-4]
        + "_"
        + os.path.basename(audio_path)[:-4]
        + ".mp4"
    )

    print(
        "make video code, output_path: ",
        output_path,
        ", stdout:",
        response.stdout,
        "stderr:",
        response.stderr,
    )

    return output_path
