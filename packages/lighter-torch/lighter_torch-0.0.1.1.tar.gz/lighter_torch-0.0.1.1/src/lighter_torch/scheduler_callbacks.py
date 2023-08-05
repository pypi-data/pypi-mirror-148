from torch.optim import lr_scheduler

from .trainer import Trainer, TrainerCallback
from .utils import is_divisor

__all__ = [
    'ScheduleBatchSize',
    'ScheduleLR',
    'StepLR',
]


class ScheduleBatchSize(TrainerCallback):
    def __init__(self, step: int, gamma: int = 2):
        self.step = step
        self.gamma = gamma

    def end_batch(self, trainer: Trainer, batch_num: int) -> None:
        if is_divisor(batch_num, self.step):
            trainer.batch_size *= self.gamma


class ScheduleLR(TrainerCallback):
    def __init__(self, lr_scheduler_cls, **kwargs):
        self.lr_scheduler_cls = lr_scheduler_cls
        self.kwargs = kwargs
        self.lr_scheduler = None

    def start_training(self, trainer: Trainer) -> None:
        self.lr_scheduler = self.lr_scheduler_cls(trainer.optim, **self.kwargs)
        trainer.callback_params['lrs'] = []

    def end_batch(self, trainer: Trainer, batch_num: int) -> None:
        self.lr_scheduler.step()


class StepLR(ScheduleLR):
    def __init__(self, step_size: int, gamma: float, last_epoch: int = -1, **kwargs):
        super().__init__(lr_scheduler.StepLR, step_size=step_size, gamma=gamma, last_epoch=last_epoch, **kwargs)
