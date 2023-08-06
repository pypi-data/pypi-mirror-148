import fsspec

from pystac.stac_io import DefaultStacIO, StacIO


class CustomIO(DefaultStacIO):
    """
    Object to perform IO tasks with a `fsspec` compatible file system.

    :param filesystem: (optional) `fsspec` compatible file system instance. If
        not provided, it will be inferred from the protocol.
    """
    def __init__(self, filesystem=None):
        self.filesystem = filesystem

    def read_text_from_href(self, href):
        """
        Read from local or remote file system.

        :param href: (str) URI where to read from.
        """
        if self.filesystem is not None:
            with self.filesystem.open(href, mode="r") as f:
                text = f.read()
        else:
            with fsspec.open(href, mode="r") as f:
                text = f.read()
        return text

    def write_text_to_href(self, href, txt):
        """
        Write to local or remote file system.

        :param href: (str) URI where to write to.
        :param txt: (str) text to be written.
        """
        if self.filesystem is not None:
            with self.filesystem.open(href, mode="w") as f:
                f.write(txt)
        else:
            with fsspec.open(href, mode="w") as f:
                f.write(txt)


def set_default_stac_io():
    """
    Register CustomIO class as default StacIO.
    """
    StacIO.set_default(CustomIO)


def configure_stac_io(filesystem=None):
    """
    Configure PySTAC to read from/write to the provided file system.

    :param filesystem: `fsspec` compatible file system instance.
    """
    return CustomIO(filesystem)
