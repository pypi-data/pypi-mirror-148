import datetime
import os
from time import strftime

import ffmpeg
import numpy as np
from loguru import logger
import sounddevice as sd
from scipy.io import wavfile

from models.audio_stream import (
    FFmpegAudioStream, 
    LiveATCStreamEgg
)
from models.recording import RecordingMode


def record_liveatc_audio_stream(flag:str, mode:str="pipe", **stream_config):
    ffmpeg_stream = get_liveatc_ffmpeg_audio_stream(flag)
    return _record_stream(ffmpeg_stream, mode=RecordingMode(mode), **stream_config)


def get_liveatc_ffmpeg_audio_stream(flag:str):
    stream_egg = LiveATCStreamEgg(flag=flag)
    probe = _get_stream_prob(stream_egg.url)
    return _get_ffmpeg_audio_stream(probe)


def _get_stream_prob(url: str):
    return ffmpeg.probe(url, loglevel='error')


def _get_ffmpeg_audio_stream(probe):
    streams = probe.get("streams", [])
    assert len(streams) == 1, 'There must be exactly one stream available'
    stream = streams[0]
    codec_type = stream.get("codec_type", None)
    assert codec_type == 'audio', 'The stream must be an audio stream'
    channels = stream.get("channels", None)
    samplerate = stream.get('sample_rate', None)
    if channels is not None:
        channels = int(channels)
    if samplerate is not None:
        samplerate = int(samplerate)
    return FFmpegAudioStream(
        url=probe['format']['filename'],
        probe=probe,
        stream=stream,
        codec_type=codec_type,
        channels=channels,
        samplerate=samplerate
    )
    
def _record_stream(
            stream: FFmpegAudioStream, 
            mode: RecordingMode,
            patient_frame: int = 3,
            playback: bool = True,
            export_dir: str = None
    ):
        if mode == RecordingMode.pipe:
            process = ffmpeg.input(
                stream.url
            ).output(
                'pipe:',
                format='f32le',
                acodec='pcm_f32le',
                ac=stream.channels,
                ar=stream.samplerate,
                loglevel='quiet',
            ).run_async(
                pipe_stdout=True
            )
            read_size = stream.channels * stream.samplerate * 4
            wait_frame = -1 # avoid triggering wait_frame == 0 for the first time
            record_frame_ls = []
            while True:
                buffer_arr = np.frombuffer(process.stdout.read(read_size), dtype=np.float32)
                avg_fluctuation = np.round(np.mean(np.abs(buffer_arr)), 3)
                if avg_fluctuation > 0:
                    wait_frame = patient_frame
                    record_frame_ls += [buffer_arr]
                    logger.debug(f"FD: {avg_fluctuation:.3f}, wait: {wait_frame}")
                else:
                    wait_frame -= 1
                    if wait_frame > 0:
                        record_frame_ls += [buffer_arr]
                        logger.debug(f"FD: {avg_fluctuation:.3f}, wait: {wait_frame}")
                if wait_frame == 0:
                    logger.info(f"Captured {len(record_frame_ls)} frames audio")
                    data = np.concatenate(record_frame_ls, axis=0)
                    # clear the record_frame
                    record_frame_ls = []
                    end_time = datetime.datetime.now().isoformat()
                    if playback is True:
                        sd.play(data, stream.samplerate, blocking=False)
                    if export_dir is not None:
                        export_path = os.path.join(export_dir, f"{stream.flag}_{end_time}.wav")
                        os.makedirs(export_dir, exist_ok=True)
                        logger.info(f"[{stream.flag}] Exporting to {export_path}")
                        wavfile.write(filename=export_path, data=data, rate=stream.samplerate)
    
        
if __name__ == "__main__":
    record_liveatc_audio_stream("kbos_twr")
    pass