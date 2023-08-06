import torch
import numpy as np
from typing import Callable
import os
from scipy.io.wavfile import write
from pydub import AudioSegment


import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages/tts')


from models.fatchord_version import WaveRNN
from utils.checkpoints import init_tts_model
from utils.dsp import DSP
from utils.text.cleaners import Cleaner
from utils.text.tokenizer import Tokenizer


class Synthesizer:

    def __init__(self,
                 tts_path: str,
                 voc_path: str,
                 device='cpu'):
        self.device = torch.device(device)
        tts_checkpoint = torch.load(tts_path, map_location=self.device)
        tts_config = tts_checkpoint['config']
        tts_model = init_tts_model(tts_config)
        tts_model.load_state_dict(tts_checkpoint['model'])
        self.tts_model = tts_model
        self.wavernn = WaveRNN.from_checkpoint(voc_path)
        self.melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        self.melgan.to(device).eval()
        self.cleaner = Cleaner.from_config(tts_config)
        self.tokenizer = Tokenizer()
        self.dsp = DSP.from_config(tts_config)

    def __call__(self,
                 text: str,
                 voc_model: str,
                 alpha=1.0,
                 pitch_function: Callable[[torch.tensor], torch.tensor] = lambda x: x,
                 energy_function: Callable[[torch.tensor], torch.tensor] = lambda x: x,
                 ) -> np.array:
        x = self.cleaner(text)
        x = self.tokenizer(x)
        x = torch.tensor(x).unsqueeze(0)
        gen = self.tts_model.generate(x,
                                      alpha=alpha,
                                      pitch_function=pitch_function,
                                      energy_function=energy_function)
        m = gen['mel_post'].cpu()
        if voc_model == 'griffinlim':
            wav = self.dsp.griffinlim(m.squeeze().numpy(), n_iter=32)
        elif voc_model == 'wavernn':
            wav = self.wavernn.generate(mels=m,
                                        batched=True,
                                        target=11_000,
                                        overlap=550,
                                        mu_law=self.dsp.mu_law)
        else:
            m = m.cuda()
            with torch.no_grad():
                wav = self.melgan.inference(m).cpu().numpy()
        return wav
synth_forward = Synthesizer(tts_path='/content/forward_step90k.pt', voc_path='/content/wave_step575k.pt')


def generate(text, voc_type):
  wav = synth_forward(text, voc_model=voc_type, alpha=1)
  write('output.wav', 22050, wav)