from fpinpy import Result, SinglyLinkedList as Slist
from pathlib import Path

class TextFile:

    @staticmethod
    def file_to_string(file: Path, encoding:str="utf-8") -> Result[str]:
        """TODO extract filesystem to be tested.
        """
        return Result.of(file)\
            .map(lambda fp: fp.resolve())\
            .map(lambda fr: fr.read_text(encoding=encoding))\

    @staticmethod
    def split_by(value: str, delimiter="\n", keepdelimiters=False, encoding:str="utf-8") -> Result[Slist[str]]:
        """Split string into lines.

            Separates elements by newline character.

            Input: any string, usually with newline characters
            Output: list whereby each element is a line
                    An empty file yields and empty list.
                    An empty line  yields an empty string.
        """
        def delim_curried_helper(isKeepDelimiters: bool):
            def delim(delimiter_str:str):
                def apply_delimiters(string: str):
                    if isKeepDelimiters:
                        concatenation = string + delimiter_str
                        return Result.of(concatenation)
                    return Result.of(string)
                return apply_delimiters
            return delim
        apply_delimiters = delim_curried_helper(keepdelimiters)(delimiter)
        return Result.of(value)\
            .flatMap(lambda s: Slist.list(s.split(sep=delimiter, maxsplit=-1)))\
            .flatMap(lambda ts: ts.traverse(lambda t: apply_delimiters(t)))
