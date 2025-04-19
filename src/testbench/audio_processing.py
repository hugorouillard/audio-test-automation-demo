import subprocess
from pathlib import Path

def convert_wav_to_mp3(input_file: Path, output_file: Path) -> None:
    """
    Convert a WAV file to MP3 format using ffmpeg.
    
    :param input_file: Path to the input .wav file.
    :param output_file: Path to the output .mp3 file.
    """
    if not input_file.exists():
        raise FileNotFoundError(f"The input file {input_file} does not exist.")

    command = [
        'ffmpeg',
        '-y',
        '-i', str(input_file),
        str(output_file)
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")