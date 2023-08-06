class RuishiBase(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class WrongPassword(RuishiBase):
    pass


class InvalidToken(RuishiBase):
    pass


class RequestError(RuishiBase):
    pass


error_dict = {
    1003: WrongPassword,
    700: InvalidToken,
    201: RequestError
}
