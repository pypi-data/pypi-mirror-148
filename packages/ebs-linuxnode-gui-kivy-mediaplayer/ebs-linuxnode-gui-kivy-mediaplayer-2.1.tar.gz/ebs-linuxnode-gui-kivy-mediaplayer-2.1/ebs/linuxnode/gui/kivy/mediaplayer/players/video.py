

from kivy.uix.video import Video
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class VideoPlayer(MediaPlayerBase):
    _extensions = ['*']

    def _play(self, filepath, loop=False, bgcolor=(0, 0, 0, 1)):
        if loop:
            eos = 'loop'
        else:
            eos = 'stop'

        self._player = Video(source=filepath, state='play',
                             eos=eos, allow_stretch=True)
        self._player.opacity = 0

        def _while_playing(*_):
            self._player.opacity = 1
        self._player.bind(texture=_while_playing)
        self._player.bind(eos=lambda *_: self._actual.stop())
        return self._player

    def _stop(self):
        if self._player:
            self._player.unload()

    def _pause(self):
        if self._player:
            self._player.state = 'pause'

    def _resume(self):
        if self._player:
            self._player.state = 'play'
