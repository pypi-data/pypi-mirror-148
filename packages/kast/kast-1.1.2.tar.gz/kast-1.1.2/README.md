# Kast
---
Seamlessly cast your local video files to chromecast type devices.
Regardless of media containers, codecs or subtitles formats.

## Features:
---
- Detect cast devices in your local network.
- Cast right away video files compliant with chromecast supported formats.
- Automatically transcode and remux incompatible video files before casting.
- Automatically convert subtitles.
- Display local preview of streamed video.
- Thanks to OS media integration, control your stream with regular remote media control applications intened for your platform.
(e.g. KDE Connect for Plasma linux desktop)

## Installation:
---

### Binary release:
- Windows - Download installer from [here](https://bitbucket.org/massultidev/kast/downloads/).
- Linux Generic - Download installation script from [here](https://bitbucket.org/massultidev/kast/downloads/).
- Linux Arch - Available at AUR under name `kast-bin`.

### PyPI release:
For satisfying user experience it is recommended to install the application in a separate virtual environment.
You can use your favorite env creation method like conda or venv.

Installation from PyPI using venv:
```sh
python -m venv /path/to/your/venv
cd /path/to/your/venv
source bin/activate
python -m pip install kast
```

### Changelog:
---
- Version: 1.1.0
    - Taskbar progress support. (Windows/Linux)
    - Taskbar preview media controls. (Windows)
- Version: 1.1.1
    - Silent fail with 4K videos fixed. - Most chromecast devices support resolution up to Full HD. All videos are now converted to satisfy that constraint. Full support for 4K devices coming in the future.

### FAQ:
---

#### Device search or stream start does not succeed at first try.
> It has been noticed that PCs connected via WiFi might encounter this issue.
Scenario is the cast device is present in local network.
However the application is unable to find or connect to it.
Usually succeeding on second or consecutive trial.
Easy solution seems to be using Ethernet connection if possible.
It is planned to improve on the matter in upcoming releases.

#### Application failed to convert some of my subtitles claiming they are in incorrect format.
> Some subtitles files might be malformed and not compliant to their formats standards.
Although other media players may still be able to interpret them correctly.
That might be due to some internal correction procedures.
Regardless the subtitles conversion module is planned to be improved in future releases.

#### Local preview does not display subtitles.
> **Short answer:**
Subtitles are not currently supported in local preview.

> **Detailed answer:**
The preview is basically a QMediaPlayer instance.
Which does not provide a way to display captions.
Not to mention numerous other issues it has brought that required specific workarounds.
So it is definitely planned to replace it in future releases.

#### I have black screen on local preview on Windows.
> **Easiest solution:**
Use binary release which comes with preinstalled fix.

> **Easy solution:**
Install codec pack like K-Lite or similar.

> **Advanced solution:**
(Read until the end!) Download `widows_qt_media_tweak.py` and run on your venv.
Keep in mind that it is a destructive patch.
Use it only if you have a separate venv for the application.

> **Explanation:**
PyQt for Windows comes with support for two different media renderers.
Direct Show and Windows Media Foundation.
The former is older and does not support properietary codecs.
Unfortunately it's used by default and not switchable for: Qt < 5.15.5
Patch from advanced solution removes Direct Show DLL to prevent Qt from loading it.

#### I see no progress on taskbar on Linux.
> Taskbar progress on Linux is supported only by selected desktop environments. (Like KDE or Unity.)
Furthermore, the application would have to be installed in either of root or user environment.
However both approaches are discouraged and binary installation is recommended.
If you don't want the binary package, please use venv.
In which case best approach would be to:
> ```sh
> # Copy desktop and icon files to user environment:
> cp -fv ${your_venv_prefix}/share/applications/* ~/.local/share/applications/
> cp -fv ${your_venv_prefix}/share/pixmaps/* ~/.local/share/pixmaps/
>
> # Create launcher script:
> echo "#!/usr/bin/sh" > ~/.local/bin/kast
> echo "source ${your_venv_prefix}/bin/activate" >> ~/.local/bin/kast
> echo "python -m kast" >> ~/.local/bin/kast
> chmod +x ~/.local/bin/kast
>
> # Remember to replace all "${your_venv_prefix}" with your actual path!
> ```

## License
MIT
