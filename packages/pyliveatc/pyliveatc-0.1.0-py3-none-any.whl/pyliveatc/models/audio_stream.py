from typing import Optional, Any
from pydantic.dataclasses import dataclass

class ArbitaryAllowConf:
    arbitrary_types_allowed = True

@dataclass
class LiveATCStreamEgg:
    flag: str
    
    @property
    def url(self) -> str:
        return f"http://d.liveatc.net/{self.flag.lower()}"

@dataclass
class LiveATCStreamInfo(LiveATCStreamEgg):
    abstract: Optional[str]
    category: Optional[str]
    metar: Optional[str]
    place: Optional[str]
    acquired_at: Optional[str]

@dataclass(config=ArbitaryAllowConf)
class FFmpegAudioStream:
    url: str
    probe: Optional[Any]
    stream: Optional[Any]
    codec_type: Optional[str]
    channels: Optional[int]
    samplerate: Optional[int]
    
