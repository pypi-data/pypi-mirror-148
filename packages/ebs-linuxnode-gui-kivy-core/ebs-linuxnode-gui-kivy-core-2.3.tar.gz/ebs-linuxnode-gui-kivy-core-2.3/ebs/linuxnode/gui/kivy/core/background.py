
import os
import shutil
import appdirs
import subprocess

from kivy.core.window import Window
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from six.moves.urllib.parse import urlparse

from kivy_garden.ebs.core.image import BleedImage
from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from .basemixin import BaseGuiMixin


class BackgroundGuiMixin(BaseGuiMixin):
    _bg_structured_prefix = 'structured:'
    _bg_separator = ':'

    def __init__(self, *args, **kwargs):
        self._bg_image = None
        self._bg_video = None
        self._bg_structured = None
        self._bg = None
        self._bg_container = None
        self._bg_current = None
        super(BackgroundGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(BackgroundGuiMixin, self).install()

        _path = os.path.abspath(os.path.dirname(__file__))
        fallback_default = os.path.join(_path, 'images/background.png')
        fallback = os.path.join(appdirs.user_config_dir(self.config.appname), 'background.png')
        if not os.path.exists(fallback):
            shutil.copy(fallback_default, fallback)

        _elements = {
            'image_bgcolor': ElementSpec('display', 'image_bgcolor', ItemSpec('kivy_color', fallback='auto')),
            'background': ElementSpec('display', 'background', ItemSpec(str, read_only=False, fallback=fallback)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    def bg_is_structured(self, value):
        return value.startswith(self._bg_structured_prefix)

    def bg_is_file(self, value):
        return not value.startswith(self._bg_structured_prefix)

    def background_set(self, fpath):
        if not fpath:
            fpath = None

        if self.bg_is_structured(fpath):
            if not hasattr(self, fpath.split(self._bg_separator)[1]):
                fpath = None
        else:
            if not os.path.exists(fpath):
                fpath = None

        if self.config.background != fpath:
            old_bg = os.path.basename(urlparse(self.config.background).path)
            if self.bg_is_file(old_bg) and self.resource_manager.has(old_bg):
                self.resource_manager.remove(old_bg)
            self.config.background = fpath

        self.gui_bg_update()

    @property
    def gui_bg_container(self):
        if self._bg_container is None:
            self._bg_container = BoxLayout()
            self.gui_main_content.add_widget(self._bg_container)
        return self._bg_container

    def gui_bg_clear(self):
        if self._bg_image:
            self.gui_bg_container.remove_widget(self._bg_image)
            self._bg_image = None
        if self._bg_structured:
            if hasattr(self._bg_structured, 'stop'):
                self._bg_structured.stop()
            self.gui_bg_container.remove_widget(self._bg_structured)
            self._bg_structured = None
        if self._bg_video:
            self._bg_video_stop()
            self._bg_video = None
        self._bg = None

    @property
    def gui_bg_image(self):
        return self._bg_image

    @gui_bg_image.setter
    def gui_bg_image(self, value):
        if not os.path.exists(value):
            return

        self.gui_bg_clear()

        self._bg_image = BleedImage(
            source=value,
            allow_stretch=True,
            keep_ratio=True,
            bgcolor=self.config.image_bgcolor
        )
        self._bg = self._bg_image
        self.gui_bg_container.add_widget(self._bg_image)

    @property
    def gui_bg_video(self):
        return self._bg_video

    def _gui_bg_video_native(self, value):
        self._bg_video = Video(
            source=value, state='play',
            allow_stretch=True,
        )

        def _when_done(*_):
            self._bg_video.state = 'play'

        self._bg_video.bind(eos=_when_done)
        self._bg = self._bg_video
        self.gui_bg_container.add_widget(self._bg_video)

    def _bg_video_pause(self):
        if isinstance(self.gui_bg, Video):
            self.gui_bg.state = 'pause'

    def _bg_video_resume(self):
        if isinstance(self.gui_bg, Video):
            self.gui_bg.state = 'play'

    def _bg_video_stop(self):
        if isinstance(self._bg_video, Video):
            self.gui_bg_container.remove_widget(self._bg_video)
            self._bg_video.unload()

    @gui_bg_video.setter
    def gui_bg_video(self, value):
        if not os.path.exists(value):
            return

        self.gui_bg_clear()
        self._gui_bg_video_native(value)

    @property
    def gui_bg_structured(self):
        return self._bg_structured

    @gui_bg_structured.setter
    def gui_bg_structured(self, value):
        if not hasattr(self, value):
            return

        self.gui_bg_clear()

        self._bg_structured = getattr(self, value)
        self._bg = self._bg_structured
        self.gui_bg_container.add_widget(self._bg_structured)

    @property
    def gui_bg(self):
        return self._bg

    @gui_bg.setter
    def gui_bg(self, value):
        self.log.info("Setting background to {value}", value=value)
        if self.bg_is_file(value) and not os.path.exists(value):
            value = self.config.background

        if value == self._bg_current:
            return

        if self.bg_is_file(value):
            _media_extentions_image = ['.png', '.jpg', '.bmp', '.gif', '.jpeg']
            if os.path.splitext(value)[1] in _media_extentions_image:
                self.gui_bg_image = value
            else:
                self.gui_bg_video = value
        else:
            self.gui_bg_structured = value.split(self._bg_separator)[1]
        self._bg_current = value

    def gui_bg_update(self):
        self.gui_bg = self.config.background

    def gui_bg_pause(self):
        self.log.debug("Pausing Background")
        self.gui_main_content.remove_widget(self._bg_container)
        if self._bg_video:
            self._bg_video_pause()

    def gui_bg_resume(self):
        self.log.debug("Resuming Background")
        if not self._bg_container.parent:
            self.gui_main_content.add_widget(self._bg_container, len(self.gui_main_content.children))
        if hasattr(self.gui_bg, 'retrigger'):
            self.gui_bg.retrigger()
        if self._bg_video:
            self._bg_video_resume()

    def stop(self):
        if self._bg_video:
            self._bg_video_stop()
        super(BackgroundGuiMixin, self).stop()

    def gui_setup(self):
        super(BackgroundGuiMixin, self).gui_setup()
        self.gui_bg = self.config.background


class OverlayWindowGuiMixin(BackgroundGuiMixin):
    # Overlay mode needs specific host support.
    # RPi :
    #   See DISPMANX layers and
    #   http://codedesigner.de/articles/omxplayer-kivy-overlay/index.html
    # Normal Linux Host :
    #   See core-x11 branch and
    #   https://groups.google.com/forum/#!topic/kivy-users/R4aJCph_7IQ
    # Others :
    #   Unknown, see
    #   - https://github.com/kivy/kivy/issues/4307
    #   - https://github.com/kivy/kivy/pull/5252
    _gui_supports_overlay_mode = False

    def __init__(self, *args, **kwargs):
        self._overlay_mode = None
        self._foundation_process = None
        super(OverlayWindowGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(OverlayWindowGuiMixin, self).install()
        _elements = {
            'overlay_mode': ElementSpec('display', 'overlay_mode', ItemSpec(bool, fallback=False)),
            'show_foundation': ElementSpec('display-rpi', 'show_foundation', ItemSpec(bool, fallback=True)),
            'dispmanx_foundation_layer': ElementSpec('display-rpi', 'dispmanx_foundation_layer', ItemSpec(int, fallback=1)),
            'foundation_image': ElementSpec('display-rpi', 'foundation_image', ItemSpec(fallback=None)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def overlay_mode(self):
        return self._overlay_mode

    @overlay_mode.setter
    def overlay_mode(self, value):
        if not self._gui_supports_overlay_mode and value:
            self.log.warn("Application tried to change overlay mode, "
                          "not supported this platform.")
            return
        if value is True:
            self._gui_overlay_mode_enter()
        else:
            self._gui_overlay_mode_exit()

    def _gui_overlay_mode_enter(self):
        self.log.info('Entering Overlay Mode')
        if self._overlay_mode:
            return
        self._overlay_mode = True
        Window.clearcolor = [0, 0, 0, 0]
        # self.gui_bg_pause()

    def _gui_overlay_mode_exit(self):
        self.log.info('Exiting Overlay Mode')
        if not self._overlay_mode:
            return
        self._overlay_mode = False
        # self.gui_bg_resume()
        Window.clearcolor = [0, 0, 0, 1]

    def stop(self):
        if self._foundation_process:
            self._foundation_process.terminate()
        super(OverlayWindowGuiMixin, self).stop()

    def gui_setup(self):
        super(OverlayWindowGuiMixin, self).gui_setup()

        if self.config.show_foundation and \
                self.config.foundation_image and \
                os.path.exists(self.config.foundation_image):
            cmd = ['pngview', '-l', str(self.config.dispmanx_foundation_layer),
                   '-n', self.config.foundation_image]
            self._foundation_process = subprocess.Popen(cmd)

        self.overlay_mode = self.config.overlay_mode
