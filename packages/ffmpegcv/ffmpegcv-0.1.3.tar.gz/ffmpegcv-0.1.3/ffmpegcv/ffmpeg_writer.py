import numpy as np
import subprocess
import warnings
import pprint
from .video_info import run_async, release_process, get_num_NVIDIA_GPUs


class FFmpegWriter:
    def __del__(self):
        if hasattr(self, 'process'):
            self.release()

    def __repr__(self):
        props = pprint.pformat(self.__dict__).replace('{',' ').replace('}',' ')
        return f'{self.__class__}\n'  + props

    @staticmethod
    def VideoWriter(filename, codec, fps, frameSize, pix_fmt):
        if codec is None:
            codec = 'libx264'
        elif not isinstance(codec, str):
            codec = 'libx264'
            warnings.simplefilter('''
                Codec should be a string. Eg `h264`, `h264_nvenc`. 
                You may used CV2.VideoWriter_fourcc, which will be ignored.
                ''')
        
        vid = FFmpegWriter()
        vid.fps, vid.size = fps, frameSize
        vid.width, vid.height = vid.size if vid.size else (None, None)
        vid.codec, vid.pix_fmt, vid.filename = codec, pix_fmt, filename
        vid.waitInit = True
        return vid

    def _init_video_stream(self):
        args = (f'ffmpeg -y -loglevel warning ' 
                f'-f rawvideo -pix_fmt {self.pix_fmt} -s {self.width}x{self.height} -r {self.fps} -i pipe: '
                f'-r {self.fps} -c:v {self.codec} -pix_fmt yuv420p "{self.filename}"')
        self.process = run_async(args)

    def write(self, img):
        if self.waitInit:
            if self.size is None:
                self.size = (img.shape[1], img.shape[0])          
            self.width, self.height = self.size
            self._init_video_stream()
            self.waitInit = False

        assert self.size == (img.shape[1], img.shape[0])
        img = img.astype(np.uint8).tobytes()
        self.process.stdin.write(img)

    def release(self):
        self.process.terminate()
        self.process.wait()


class FFmpegWriterNV(FFmpegWriter):
    @staticmethod
    def VideoWriter(filename, codec, fps, frameSize, pix_fmt, gpu):
        numGPU = get_num_NVIDIA_GPUs()
        assert numGPU
        gpu = int(gpu) % numGPU if gpu is not None else 0
        if codec is None:
            codec = 'hevc_nvenc'
        elif not isinstance(codec, str):
            codec = 'hevc_nvenc'
            warnings.simplefilter('''
                Codec should be a string. Eg `h264`, `h264_nvenc`. 
                You may used CV2.VideoWriter_fourcc, which will be ignored.
                ''')
        elif codec.endswith('_nvenc'):
            codec = codec
        else:
            codec = codec + '_nvenc'
        assert codec in ['hevc_nvenc', 'h264_nvenc'], 'codec should be `hevc_nvenc` or `h264_nvenc`'

        vid = FFmpegWriterNV()
        vid.fps, vid.size = fps, frameSize
        vid.width, vid.height = vid.size if vid.size else (None, None)
        vid.codec, vid.pix_fmt, vid.filename = codec, pix_fmt, filename
        vid.gpu = gpu
        vid.waitInit = True
        return vid

    def _init_video_stream(self):
        args = (f'ffmpeg -y -loglevel warning '
            f'-f rawvideo -pix_fmt {self.pix_fmt} -s {self.width}x{self.height} -r {self.fps} -i pipe: '
            f'-r {self.fps} -gpu {self.gpu} -c:v {self.codec} -pix_fmt yuv420p "{self.filename}"')
        self.process = run_async(args)