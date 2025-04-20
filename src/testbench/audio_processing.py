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


def amplify_audio(input_path: Path, output_path: Path, gain_db: float) -> None:
    """
    Amplify the audio by a given number of decibels.

    :param input_path: Path to the input .wav file
    :param output_path: Path to the output .wav file
    :param gain_db: Volume increase in decibels (e.g., 5.0 for +5 dB)
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-filter:a", f"volume={gain_db}dB",
        str(output_path)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr.strip()}")

def normalize_audio(input_path: Path, output_path: Path) -> None:
    """
    Normalize audio to 0 dBFS using FFmpeg's loudnorm filter.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-filter:a", "loudnorm",
        str(output_path)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr.strip()}")

def process_audio_pipeline(input_path: Path, final_output_path: Path, gain_db: float = 5.0) -> None:
    """
    Apply a chain of audio processing: normalize → amplify → convert.
    """
    temp_normalized = input_path.parent / "normalized.wav"
    temp_amplified = input_path.parent / "amplified.wav"

    normalize_audio(input_path, temp_normalized)
    amplify_audio(temp_normalized, temp_amplified, gain_db=gain_db)
    convert_wav_to_mp3(temp_amplified, final_output_path)
