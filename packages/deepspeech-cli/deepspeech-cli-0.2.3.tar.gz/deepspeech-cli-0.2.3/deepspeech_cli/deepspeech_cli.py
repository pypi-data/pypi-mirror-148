#!/usr/bin/env python3

from pathlib import Path
import subprocess, typer
from enum import Enum
from . import logger, __app_name__, __version__

from .config import default, models

logger.info(f'Using config DEFAULT: {default}')
logger.info(f'Using config models: {models}')

# deepspeech_path = '/usr/local/Caskroom/miniconda/base/envs/speech/bin/deepspeech'
# deepspeech_dir = Path.home() / 'testdir/deepspeech'
deepspeech_path = default['deepspeech_path']
deepspeech_path = str(Path(default['deepspeech_path']).expanduser())
deepspeech_dir = default['deepspeech_dir']
deepspeech_dir = Path(default['deepspeech_dir']).expanduser()

app = typer.Typer()


def version_callback(version: bool | None):
    if version:
        typer.echo(f'{__app_name__} version: {__version__}')
        raise typer.Exit()


class Lang(str, Enum):
    en = 'en'
    zh = 'zh'


def convert_audio_to_wav(path: Path) -> Path:
    """
    Convert audio file to wav format.
    """
    if path.suffix == '.wav':
        return path
    else:
        # -y: overwrites without asking
        # -ac 1: mono
        # -ar 16000: 16kHz
        rc = subprocess.run([
            'ffmpeg', '-i',
            str(path), '-ar', '16000', '-y',
            str(path.with_suffix('.wav'))
        ]).returncode
        if rc != 0:
            typer.echo(f'Failed to convert {path} to wav format.', err=True)
            raise typer.Abort()
        return path.with_suffix('.wav')


@app.command()
def transcribe(path: Path = typer.Argument(...,
                                           help='Path to audio file',
                                           callback=convert_audio_to_wav),
               lang: Lang = typer.Option(Lang.en,
                                         '--lang',
                                         '-l',
                                         help='Language of the audio file'),
               version: bool = typer.Option(None,
                                            '--version',
                                            '-V',
                                            callback=version_callback,
                                            is_eager=True)):
    """Transcribe audio file"""

    if lang == Lang.en:
        model_config = models['en']
        # model = 'deepspeech-0.9.3-models.pbmm'
        # scorer = 'deepspeech-0.9.3-models.scorer'

    elif lang == Lang.zh:
        model_config = models['zh']
        # model = 'deepspeech-0.9.3-models-zh-CN.pbmm'
        # scorer = 'deepspeech-0.9.3-models-zh-CN.scorer'
    model = model_config['model_path']
    scorer = model_config['scorer_path']

    program = [
        deepspeech_path, '--model', model, '--scorer', scorer, '--audio',
        str(path.resolve())
    ]
    logger.info(f'Running {program}')

    proc = subprocess.run(program, cwd=deepspeech_dir, capture_output=True)
    if proc.returncode != 0:
        typer.echo(f'Failed to transcribe {path}', err=True)
        typer.echo(proc.stderr.decode('utf-8'), err=True)
        raise typer.Abort()
    output_path = path.with_suffix('.txt')
    output_path.write_text(proc.stdout.decode('utf-8'))
    typer.echo(f'Output saved to: {str(output_path)}')


if __name__ == '__main__':
    app()
