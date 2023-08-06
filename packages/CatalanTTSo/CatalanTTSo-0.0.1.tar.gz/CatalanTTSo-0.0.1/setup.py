from setuptools import setup, find_packages
import codecs
import os


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



VERSION = '0.0.1'
DESCRIPTION = 'Catalan Text to Speech'
# Setting up
setup(
    name="CatalanTTSo",
    version=VERSION,
    author="Mehdi Hosseini Moghadam",
    author_email="<m.h.moghadam1996@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["numba==0.49.1",
                      "librosa==0.7.2",
                      "pyworld >= 0.2.10",
                      "torch>=1.2.0",
                      "phonemizer>=2.2",
                      "webrtcvad>=2.0.10",
                      "PyYAML>=5.1",
                      "dataclasses",
                      "soundfile",
                      "scipy",
                      "tensorboard",
                      "matplotlib",
                      "unidecode",
                      "inflect",
                      "pydub"
                      ],
    keywords=[  "Catalan Text To Speech",
                "Catalan TTS",
                "Catalan" ,
                "Catalan Speech",
                "Catalan Speech Synthesis",
                "Catalan Speech To Text",
                "Catalan A.I.",
                "Catalan Speech DataSet",
                "Melgan",
                "Catalan Speech Vocoder",
                "Catalan Tacotron",
                "Catalan FastSpeech",
                "Catalan Speech To Text",
                "Catalan ASR",
                "Catalan Tacotron2"
              ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)










