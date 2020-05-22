from abc import ABC, abstractmethod


class Detector(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def detect(self, image):
        raise NotImplementedError

    @abstractmethod
    def get_name(self):
        return 'Untitled'
