from abc import abstractmethod, ABC
from concurrent.futures import Future

from pubsub.Message import Message


class PublisherClient(ABC):

    @abstractmethod
    def publish(self, message: Message) -> Future:
        pass

    @abstractmethod
    def close(self):
        pass
