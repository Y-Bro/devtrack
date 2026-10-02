from django.db import models

# Create your models here.

from abc import ABC, abstractmethod


class BaseEnitity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}
