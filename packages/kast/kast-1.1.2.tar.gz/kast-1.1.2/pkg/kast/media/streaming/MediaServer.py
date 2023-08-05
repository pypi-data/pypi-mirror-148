#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J.

import contextlib
import socket
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import bottle

from kast.media.streaming.ServerAdapter import ServerAdapter
from kast.utils.Loggable import Loggable


@dataclass
class MediaContent:
    movieFile: Optional[Path] = None
    subtitlesFile: Optional[Path] = None
    thumbnailFile: Optional[Path] = None


class MediaServer(Loggable):

    URL_MEDIA = '/media'
    URL_MOVIE = URL_MEDIA + '/movie'
    URL_SUBTITLES = URL_MEDIA + '/subtitles'
    URL_THUMBNAIL = URL_MEDIA + '/thumbnail'

    def __init__(self) -> None:
        self._host = self._getHost()
        self._port = self._getPort()

        self._webApp = bottle.Bottle()
        self._server = ServerAdapter(host=self._host, port=self._port)

        self._thread: Optional[threading.Thread] = None

        self._mediaContent = MediaContent()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        self._server.stop()
        self._thread.join()

    @property
    def mediaContent(self) -> MediaContent:
        return self._mediaContent

    @property
    def movieUrl(self) -> Optional[str]:
        movieFile = self.mediaContent.movieFile
        return None if movieFile is None else self._getUrl(
            urlBase=self.URL_MOVIE,
            fileName='movie',
            extension=self._getExtWithoutComa(movieFile)
            )

    @property
    def subtitleUrl(self) -> Optional[str]:
        subtitlesFile = self.mediaContent.subtitlesFile
        return None if subtitlesFile is None else self._getUrl(
            urlBase=self.URL_SUBTITLES,
            fileName='subtitles',
            extension=self._getExtWithoutComa(subtitlesFile)
        )

    @property
    def thumbnailUrl(self) -> Optional[str]:
        thumbnailFile = self.mediaContent.thumbnailFile
        return None if thumbnailFile is None else self._getUrl(
            urlBase=self.URL_THUMBNAIL,
            fileName='thumbnail',
            extension=self._getExtWithoutComa(thumbnailFile)
        )

    def _run(self) -> None:
        web = self._webApp

        @web.get(self.URL_MOVIE + '/<name>.<ext>')
        def movie(name: str, ext: str) -> bottle.Response:
            return self._serveFile(self.mediaContent.movieFile)

        @web.get(self.URL_SUBTITLES + '/<name>.<ext>')
        def subtitles(name: str, ext: str) -> bottle.Response:
            return self._serveFile(self.mediaContent.subtitlesFile)

        @web.get(self.URL_THUMBNAIL + '/<name>.<ext>')
        def thumbnail(name: str, ext: str) -> bottle.Response:
            return self._serveFile(self.mediaContent.thumbnailFile)

        self._webApp.run(server=self._server, quiet=True)

    def _serveFile(self, filePath: Path) -> bottle.Response:
        if not filePath:
            return bottle.HTTPError(410, 'Resource no longer available.')
        response = bottle.static_file(filename=filePath.name, root=filePath.parent)

        if 'Last-Modified' in response.headers:
            del response.headers['Last-Modified']

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return response

    def _getUrl(self, urlBase: str, fileName: str, extension: str) -> str:
        return f"http://{self._host}:{self._port}{urlBase}/{fileName}.{extension}"

    @staticmethod
    def _getExtWithoutComa(filePath: Path) -> str:
        return filePath.suffix.split('.', maxsplit=1)[-1]

    @staticmethod
    def _getHost() -> str:
        hostIps = socket.gethostbyname_ex(socket.gethostname())[2]
        hostIps = [ip for ip in hostIps if not ip.startswith("127.")]
        if hostIps:
            return hostIps[0]

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 53))
            return sock.getsockname()[0]

    @staticmethod
    def _getPort() -> int:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('0.0.0.0', 0))
            return s.getsockname()[1]
