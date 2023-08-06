from abc                            import ABC, abstractmethod


class ABCMessage(ABC):

    def process_email_msg(self, message):
        is_valid = self.validate_email_msg(message)
        if is_valid:
            self.send_email_notification()
        return is_valid

    def validate_email_msg(self, message):
        pass

    @classmethod
    @abstractmethod
    def send_email_notification(self):
        pass
