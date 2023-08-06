#!/usr/bin/env python3
"""
parse config from the config file at ~/.deepspeech_cli.ini
"""
import configparser
import os
from pathlib import Path

DEFAULT_MODEL_VERSION = '0.9.3'


def get_config_path(envvar_name: str, default_path: Path) -> Path:
    """
    Get the path to the config file.
    """
    config_path = os.environ.get(envvar_name)
    if config_path is None:
        config_path = default_path
    return Path(config_path)


def parse_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


config_path = get_config_path('DEEPSPEECH_CLI_CONFIG',
                              Path.home() / '.deepspeech_cli.ini')
config = parse_config(config_path)

default = dict(deepspeech_path=config.get('DEFAULT',
                                          'deepspeech_path',
                                          fallback='deepspeech'),
               ffmpeg_path=config.get('DEFAULT',
                                      'ffmpeg_path',
                                      fallback='ffmpeg'),
               deepspeech_dir=config.get('DEFAULT',
                                         'deepspeech_dir',
                                         fallback=str(Path.cwd())))


def get_deepspeech_version(deepspeech_path: str) -> str:
    """
    Get the version of deepspeech.
    """
    import subprocess
    version = subprocess.run(
        [deepspeech_path, '--version'],
        stdout=subprocess.PIPE).stdout.decode('utf-8').split()[1]
    return version.strip()


def get_language_model_config(
        model_version: str | None = DEFAULT_MODEL_VERSION,
        config: configparser.ConfigParser = config) -> dict:
    model_version = model_version or DEFAULT_MODEL_VERSION
    en = dict(model_path=config.get(
        'en', 'model_path',
        fallback=f'deepspeech-{model_version}-models.pbmm'),
              scorer_path=config.get(
                  'en',
                  'scorer_path',
                  fallback=f'deepspeech-{model_version}-models.scorer'))

    zh = dict(model_path=config.get(
        'zh',
        'model_path',
        fallback=f'deepspeech-{model_version}-models-zh-CN.pbmm'),
              scorer_path=config.get(
                  'zh',
                  'scorer_path',
                  fallback=f'deepspeech-{model_version}-models-zh-CN.scorer'))

    return dict(en=en, zh=zh)


models = get_language_model_config(config.get('DEFAULT', 'model_version'))