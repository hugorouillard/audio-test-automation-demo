import subprocess
from pathlib import Path
from testbench.audio_processing import convert_wav_to_mp3, amplify_audio, process_audio_pipeline


def generate_dummy_wav(path: Path):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=1",
        str(path)
    ], capture_output=True, text=True, check=True)


def test_convert_wav_to_mp3(tmp_path):
    input_wav = tmp_path / "input.wav"
    output_mp3 = tmp_path / "output.mp3"

    generate_dummy_wav(input_wav)
    convert_wav_to_mp3(input_wav, output_mp3)

    assert output_mp3.exists()


def test_amplify_audio(tmp_path):
    input_wav = tmp_path / "input.wav"
    output_wav = tmp_path / "amplified.wav"

    generate_dummy_wav(input_wav)
    amplify_audio(input_wav, output_wav, gain_db=5.0)

    assert output_wav.exists()


def get_duration(path: Path) -> float:
    """
    Get audio duration in seconds using ffprobe.
    """
    result = subprocess.run([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ], capture_output=True, text=True)

    return float(result.stdout.strip())


def test_process_audio_pipeline(tmp_path):
    input_wav = tmp_path / "input.wav"
    output_mp3 = tmp_path / "final.mp3"

    generate_dummy_wav(input_wav)  # 1s sine wave
    process_audio_pipeline(input_wav, output_mp3)

    assert output_mp3.exists()

    # Validate duration hasn't drifted much
    input_duration = get_duration(input_wav)
    output_duration = get_duration(output_mp3)
    assert abs(input_duration - output_duration) < 0.1