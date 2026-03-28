from ._base import BaseMiddleware

class PlanAgentMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)