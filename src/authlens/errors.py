"""Safe machine codes; raw input must never enter diagnostic messages."""


class AuthLensError(Exception):
    def __init__(self, code: str, exit_code: int = 2):
        self.code = code
        self.exit_code = exit_code
        super().__init__(code)
