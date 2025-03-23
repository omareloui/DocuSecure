from abc import abstractmethod


class IParser:
    @abstractmethod
    def parse(self, path):
        raise NotImplementedError


class TextParser(IParser):
    def parse(self, path):
        with open(path) as f:
            s = f.read()
        return s


class FileParser:
    def __init__(self, parser):
        if not isinstance(parser, IParser):
            raise Exception("Invalid interface.")

        self._parser = parser

    def parse(self, path):
        return self._parser.parse(path)


def get_parser_from_mimetype(mimetype):
    match mimetype:
        case "application/json" | "text/plain" | "text/csv":
            return TextParser()
        case _:
            raise Exception("Not supported mimetype.")
