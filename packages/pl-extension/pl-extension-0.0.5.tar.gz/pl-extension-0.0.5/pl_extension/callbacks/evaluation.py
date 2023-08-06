import logging

from pytorch_lightning.callbacks.base import Callback

__all__ = ["Evaluation"]

logger = logging.getLogger(__name__)


class Evaluation(Callback):

    r"""
    Evaluation callback. Do evaluation after testing.
    """

    def on_validation_start(self, trainer, pl_module):
        if trainer.running_sanity_check or not pl_module.do_validation:
            return
        logger.info("Run validation ...")

    def on_validation_batch_end(
        self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx
    ):
        if len(trainer.num_val_batches) > 1:
            raise NotImplementedError
        if trainer.running_sanity_check or not pl_module.do_validation:
            return
        num_batch = trainer.num_val_batches[0]
        if batch_idx % pl_module.log_every_n_steps_in_valid == 0:
            logger.info(f"{batch_idx} / {num_batch}")

    def on_validation_end(self, trainer, pl_module):
        """
        Do evaluation when valid finished.
        """
        if trainer.running_sanity_check or not pl_module.do_validation:
            return
        if not pl_module.evaluation_when_valid:
            return
        if hasattr(pl_module, "report_metric"):
            pl_module.report_metric()

    def on_test_start(self, trainer, pl_module):
        logger.info("Run test ...")

    def on_test_batch_end(
        self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx
    ):
        if len(trainer.num_test_batches) > 1:
            raise NotImplementedError
        num_batch = trainer.num_test_batches[0]
        if batch_idx % pl_module.log_every_n_steps_in_test == 0:
            logger.info(f"{batch_idx} / {num_batch}")

    def on_test_end(self, trainer, pl_module):
        """
        Do evaluation when test finished.
        """
        if hasattr(pl_module, "report_metric"):
            pl_module.report_metric()
