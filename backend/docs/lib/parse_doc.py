from abc import abstractmethod

import docx
from pypdf import PdfReader


class IParser:
    @abstractmethod
    def parse(self, path):
        raise NotImplementedError


class PdfParser(IParser):
    def parse(self, path):
        reader = PdfReader(path)
        text = ""
        for p in reader.pages:
            text += p.extract_text()
        return text


class WordParser(IParser):
    def parse(self, path):
        doc = docx.Document(path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return "\n".join(fullText)


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
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return WordParser()
        case "application/pdf":
            return PdfParser()
        case "application/json" | "text/plain" | "text/csv":
            return TextParser()
        case _:
            raise Exception(f'"{mimetype}" is not supported mimetype.')
