from auicommon.audio.types import PcmAudio
from auicommon.util.textnorm import map_star_hash

def test_pcm_audio():
    pcm = PcmAudio(data=b'1234', rate=16000)
    assert pcm.rate == 16000

def test_map_star_hash():
    text = 'Taste * und #'
    assert 'Stern' in map_star_hash(text)
    assert 'Raute' in map_star_hash(text)
