import logging

from pytorch_lightning.callbacks.base import Callback

__all__ = ["LinearScalingRule"]

logger = logging.getLogger(__name__)


class LinearScalingRule(Callback):

    r"""
    Linear scaling learning rate rule, following :paper:`ImageNet in 1h`.
    BYW, it also print epoch size.

    Args:
        reference_world_size: reference world size, LinearScalingRule is only
            available when reference_world_size > 0 and 'ddp' is used.

    Example::

        from pl_extension.callbacks import LinearScalingRule
        linear_callback = LinearScalingRule(1)
        trainer = Trainer(callbacks=[linear_callback])

    """

    def __init__(self, reference_world_size: int):
        self.reference_world_size = reference_world_size

    def on_train_start(self, trainer, pl_module):
        self.__show_epoch_size(trainer)
        if self.reference_world_size == 0:
            return
        scale = trainer.world_size // self.reference_world_size
        # TODO: log info about only support ddp mode
        msg = "LinearScalingRule: "
        # batch size
        if hasattr(trainer.datamodule, "batch_size"):
            # batch_size is not multiplied by scale, because
            # trainer.datamodule.batch_size is actually batch_size_per_gpu.
            # When in ddp, total_batch_size = batch_size_per_gpu * scale,
            # which is done by ddp, so we skip here.
            msg, _ = self.__update(
                trainer.datamodule.batch_size,
                trainer.datamodule.batch_size * scale,
                msg,
                "batch_size",
            )
            total_batch_size = trainer.datamodule.batch_size * scale
        else:
            total_batch_size = scale
        # learning rate
        lr_scale = total_batch_size
        msg, lr = self.__update(
            trainer.optimizers[0].param_groups[0]["lr"],
            trainer.optimizers[0].param_groups[0]["lr"] * lr_scale,
            msg,
            "learning_rate",
        )
        trainer.optimizers[0].param_groups[0]["lr"] = lr
        # max steps
        if trainer.max_steps:
            msg, max_steps = self.__update(
                trainer.max_steps, trainer.max_steps // scale, msg, "max steps"
            )
            trainer.max_steps = max_steps
        # min steps
        if trainer.min_steps:
            msg, min_steps = self.__update(
                trainer.min_steps, trainer.min_steps // scale, msg, "min steps"
            )
            trainer.min_steps = min_steps
        # TODO: warmup steps
        logger.info(msg[:-2])  # ignore last ", "

    def __update(self, old_value, new_value, msg, name):
        msg += f"{name}: {old_value} => {new_value}, "
        return msg, new_value

    def __show_epoch_size(self, trainer):
        epoch_size = trainer.num_training_batches
        logger.info(f"epoch size: {epoch_size}")
