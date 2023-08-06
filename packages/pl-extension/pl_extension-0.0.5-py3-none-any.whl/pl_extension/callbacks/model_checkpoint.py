import logging

from pytorch_lightning.callbacks import ModelCheckpoint as _ModelCheckpoint

__all__ = ["ModelCheckpoint"]

logger = logging.getLogger(__name__)


class ModelCheckpoint(_ModelCheckpoint):

    r"""
    ModelCheckpoint same as pl, plus logging and train_epoch_end callback.

    1. log output when save checkpoint.
    2. add train_epoch_end callback.

    """

    def __init__(self, *args, **kwargs):
        self.on_epoch = kwargs.pop("on_epoch", False)
        super(ModelCheckpoint, self).__init__(*args, **kwargs)

    def on_train_epoch_end(self, trainer, pl_module, outputs):
        """
        save checkpoint every epoch end.
        """
        if self.on_epoch:
            self.save_checkpoint(trainer, pl_module)

    def save_checkpoint(self, trainer, pl_module):
        super(ModelCheckpoint, self).save_checkpoint(trainer, pl_module)
        epoch = trainer.current_epoch
        global_step = trainer.global_step
        monitor_candidates = self._monitor_candidates(trainer)
        filepath = self.format_checkpoint_name(
            epoch, global_step, monitor_candidates
        )
        if self._fs.exists(filepath):
            logger.info(f"Save checkpoint to {filepath}")
