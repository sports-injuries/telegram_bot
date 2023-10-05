class AppError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
