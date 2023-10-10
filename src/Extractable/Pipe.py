import abc

from src.Extractable.Dataobj import DataObj


class Pipe(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process(input_obj: DataObj) -> DataObj:
        return input_obj
