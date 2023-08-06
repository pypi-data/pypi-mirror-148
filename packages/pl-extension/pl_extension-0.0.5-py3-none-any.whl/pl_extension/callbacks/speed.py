import logging

from pytorch_lightning.callbacks.base import Callback

__all__ = ["Speed"]

logger = logging.getLogger(__name__)


class Speed(Callback):

    r"""
    Training speed callback, require 'simple' or 'advanced' profiler.

    """

    def on_train_batch_end(
        self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx
    ):
        legacy_metrics = (
            trainer.logger_connector.cached_results.legacy_batch_log_metrics
        )
        legacy_metrics["iter"] = trainer.global_step
        legacy_metrics["epoch"] = trainer.current_epoch
        if not self.__has_profiler(trainer):
            # if not profiler provided, skip speed and batch_time.
            return
        # get training one batch time
        run_training_batch_time = trainer.profiler.recorded_durations[
            "run_training_batch"
        ][-1]
        if hasattr(trainer.datamodule, "batch_size"):
            total_batch_size = (
                trainer.datamodule.batch_size * trainer.world_size
            )
            legacy_metrics["speed"] = (
                1.0 * total_batch_size / run_training_batch_time
            )
        else:
            legacy_metrics["batch_time"] = run_training_batch_time

    def on_train_epoch_end(self, trainer, pl_module, *args, **kwargs):
        if not self.__has_profiler(trainer):
            return
        run_training_epoch_time = trainer.profiler.recorded_durations[
            "run_training_epoch"
        ]
        if len(run_training_epoch_time) > 0 and hasattr(
            trainer.logger, "log_metrics"
        ):
            epoch_time = {"epoch_time": run_training_epoch_time[-1]}
            trainer.logger.log_metrics(epoch_time, step=trainer.current_epoch)

    def __has_profiler(self, trainer):
        return hasattr(trainer.profiler, "recorded_durations")
