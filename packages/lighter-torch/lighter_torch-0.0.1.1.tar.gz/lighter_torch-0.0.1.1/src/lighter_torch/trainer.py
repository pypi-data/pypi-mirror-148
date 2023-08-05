from typing import Tuple, Iterable, Any, Union
from collections import defaultdict

from tqdm import trange
import numpy as np

import torch
from torch.nn import Module

from .utils import is_divisor

__all__ = [
    'Trainer',
    'TrainerCallback',
    'Dataloader',
]


class Trainer(object):
    def __init__(self, model: Module, loader: 'Dataloader', lr: float, batch_size: int, **kwargs):
        self.model = model
        self.loader = loader
        self.batch_size = batch_size

        self.optim = self.configure_optimizer(lr=lr)
        self.losses = defaultdict(list)

        self.callback_params = {}
        self.lrs = []

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.init()

    def init(self):
        pass

    def train_epoch(self,
                    num_batches: int,
                    callbacks: Tuple['TrainerCallback', ...] or 'TrainerCallback' = (),
                    disable_tqdm: bool = False,
                    update_tqdm_freq: int = 10,
                    ):

        if isinstance(callbacks, TrainerCallback):
            callbacks = (callbacks, )

        callbacks = _StackedTrainerCallbacks(list(callbacks) + [self.loader])

        pbar = trange(num_batches, disable=disable_tqdm)

        callbacks.start_training(self)

        for batch_num in pbar:
            self.model.train()
            self.optim.zero_grad()
            batch_data = self.get_batch(batch_num)
            loss_dict = self.get_loss_dict(batch_data)
            loss = sum(loss_dict.values())
            loss.backward()
            self.optim.step()

            self._update_losses(loss_dict, loss)
            self.lrs.append(self.lr)

            if not disable_tqdm:
                self._update_tqdm(pbar, batch_num, update_tqdm_freq)

            break_epoch = callbacks.end_batch(self, batch_num)

            if break_epoch:
                break

        callbacks.end_training(self)

    def _update_tqdm(self, pbar, batch_num: int, update_tqdm_freq: int):
        if is_divisor(batch_num, update_tqdm_freq):
            last_loss = np.mean(self.losses['total_loss'][-10:])
            pbar.set_description(f'Loss = {last_loss:.2e}')

    def get_batch(self, batch_num: int) -> Any:
        return self.loader.get_batch(self.batch_size)

    def get_loss_dict(self, batch_data) -> dict:
        pass

    def _update_losses(self, loss_dict, loss) -> None:
        for k, v in loss_dict.items():
            self.losses[k].append(v.item())

        self.losses['total_loss'].append(loss.item())

    def configure_optimizer(self, lr: float) -> torch.optim.Optimizer:
        optim = torch.optim.AdamW(self.model.parameters(), lr)
        return optim

    @property
    def lr(self) -> float:
        return self.optim.param_groups[0]['lr']

    @lr.setter
    def lr(self, lr: float) -> None:
        self.optim.param_groups[0]['lr'] = lr


class TrainerCallback(object):
    def start_training(self, trainer: Trainer) -> None:
        pass

    def end_training(self, trainer: Trainer) -> None:
        pass

    def end_batch(self, trainer: Trainer, batch_num: int) -> Union[bool, None]:
        pass


class Dataloader(TrainerCallback):
    def get_batch(self, batch_num: int) -> Any:
        pass

    def __getitem__(self, batch_num: int) -> Any:
        return self.get_batch(batch_num)


class _StackedTrainerCallbacks(TrainerCallback):
    def __init__(self, callbacks: Iterable[TrainerCallback]):
        self.callbacks = tuple(callbacks)

    def start_training(self, trainer: Trainer) -> None:
        for c in self.callbacks:
            c.start_training(trainer)

    def end_training(self, trainer: Trainer) -> None:
        for c in self.callbacks:
            c.end_training(trainer)

    def end_batch(self, trainer: Trainer, batch_num: int) -> Union[bool, None]:
        break_epoch = False
        for c in self.callbacks:
            break_epoch += bool(c.end_batch(trainer, batch_num))
        return break_epoch
