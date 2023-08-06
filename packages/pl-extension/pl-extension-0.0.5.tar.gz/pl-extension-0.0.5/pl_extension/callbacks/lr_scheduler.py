import copy
from typing import Dict

import mmcv
from easydict import EasyDict as edict
from mmcv.runner.hooks import HOOKS
from pytorch_lightning.callbacks.base import Callback

__all__ = ["LRScheduler"]


class LRScheduler(Callback):

    r"""
    Learning rate scheduler, using mmcv. In mmcv, learning rate
    scheduler is implemented by hook. We need to re-use mmcv
    in lightning, so Callback is used instead.

    Args:
        cfg: learning rate config, in mmcv-fashion.

    Example::

        from pl_extension.callbacks import LRScheduler
        lr_config=dict(
            policy='step',
            warmup='linear',
            warmup_ratio=0.001,
            warmup_iters=1,
            warmup_by_epoch=True,
            step=[21, 26, 28],
            contrib='mmcv',
        )
        lr_callback = LRScheduler(lr_config)
        trainer = Trainer(callbacks=[lr_callback])

    """

    def __init__(self, cfg: Dict):
        lr_config = copy.deepcopy(cfg)
        assert "contrib" in lr_config
        assert lr_config.pop("contrib") == "mmcv"
        # copy-and-paste from mmcv.runner.BaseRunner.register_lr_hook
        assert "policy" in lr_config
        policy_type = lr_config.pop("policy")
        # If the type of policy is all in lower case, e.g., 'cyclic',
        # then its first letter will be capitalized, e.g., to be 'Cyclic'.
        # This is for the convenient usage of Lr updater.
        # Since this is not applicable for `
        # CosineAnnealingLrUpdater`,
        # the string will not be changed if it contains capital letters.
        if policy_type == policy_type.lower():
            policy_type = policy_type.title()
        hook_type = policy_type + "LrUpdaterHook"
        lr_config["type"] = hook_type
        self.hook = mmcv.build_from_cfg(lr_config, HOOKS)
        self.runner = None

    def on_train_start(self, trainer, pl_module):
        """
        before_run in hook.
        """
        self.runner = self.__build_runner_from_trainer(trainer)
        self.hook.before_run(self.runner)

    def on_train_epoch_start(self, trainer, pl_module):
        """
        before_train_epoch in hook.
        """
        self.runner = self.__build_runner_from_trainer(trainer)
        self.runner.epoch = trainer.current_epoch
        self.runner.data_loader = trainer.train_dataloader
        self.hook.before_train_epoch(self.runner)

    def on_train_batch_start(self, trainer, *args, **kwargs):
        """
        before_train_iter in hook.
        """
        self.runner = self.__build_runner_from_trainer(trainer)
        self.runner.epoch = trainer.current_epoch
        self.runner.iter = trainer.global_step
        self.hook.before_train_iter(self.runner)
        # log learning rate
        legacy_metrics = (
            trainer.logger_connector.cached_results.legacy_batch_log_metrics
        )
        legacy_metrics["lr"] = trainer.optimizers[0].param_groups[0]["lr"]

    def __build_runner_from_trainer(self, trainer):
        """
        build runner(mmcv) from trainer(lightning).
        """
        if self.runner:
            return self.runner
        runner = edict()
        # Use first optimizer if multi optimizers provided.
        runner.optimizer = trainer.optimizers[0]
        runner.iter = trainer.global_step
        runner.epoch = trainer.current_epoch
        runner.max_epochs = trainer.max_epochs
        if trainer.max_steps:
            runner.max_iters = trainer.max_steps
        else:
            runner.max_iters = trainer.max_epochs * len(
                trainer.train_dataloader
            )  # noqa
        return runner
