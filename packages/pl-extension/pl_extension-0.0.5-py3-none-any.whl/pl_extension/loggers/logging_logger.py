import os
from typing import List

from pl_extension.utilities.logger import setup_logger
from pl_extension.utilities.rand import time_string

from pytorch_lightning.loggers.base import LightningLoggerBase
from pytorch_lightning.utilities import rank_zero_only

__all__ = ["LoggingLogger"]


class LoggingLogger(LightningLoggerBase):

    """
    Logging logger.

    Args:
        logdir: local logs save path.
        prefix: logfile name prefix, default is 'pl'.
        skip_metrics: skip certain metric, useful for iter-wise metrics.

    Example::

        from pl_extension.loggers import LoggingLogger
        logging_logger = LoggingLogger(logdir='logs', prefix='pl_extension')
        trainer = Trainer(logger=[logging_logger])

    """

    def __init__(
        self,
        logdir: str = ".pl_extension_logs",
        *,
        prefix: str = "pl",
        skip_metrics: List = [],
    ):
        super().__init__()
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        logfile = os.path.join(logdir, f"{prefix}-{time_string()}.log")
        self._experiment = setup_logger(logfile, name=prefix)
        self._skip_metrics = skip_metrics

    def __getattr__(self, name):
        if name == "logger":
            self.experiment.warning(
                "xxx.logger is deprecated, " "please use xxx.experiment instead"
            )
            return self.experiment

    @property
    @rank_zero_only
    def experiment(self):
        return self._experiment

    @rank_zero_only
    def info(self, *args, **kwargs):
        self._experiment.info(*args, **kwargs)

    @rank_zero_only
    def warning(self, *args, **kwargs):
        self._experiment.warning(*args, **kwargs)

    @rank_zero_only
    def error(self, *args, **kwargs):
        self._experiment.error(*args, **kwargs)

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # skip metric in list
        metrics = {
            k: metrics[k] for k in metrics if k not in self._skip_metrics
        }
        _str = ""
        if "epoch" in metrics:
            _str += "Epoch[%d] " % metrics.pop("epoch")
        if "iter" in metrics:
            _str += "Iter[%d] " % metrics.pop("iter")
        else:
            _str += "Step[%d] " % step
        if "speed" in metrics:
            _str += "Speed: %.2f samples/sec, " % metrics.pop("speed")
        for k in metrics:
            if isinstance(metrics[k], int):
                _format = "%s=%d, "
            elif isinstance(metrics[k], float):
                if k == "lr":
                    _format = "%s=%.6f, "
                else:
                    _format = "%s=%.4f, "
            else:
                raise ValueError(f"Unknown value type: {type(metrics[k])}")
            _str += _format % (k, metrics[k])
        if _str:
            _str = _str[:-2]
            self.experiment.info(_str)

    @rank_zero_only
    def log_hyperparams(self, params):
        pass

    @property
    def name(self):
        return "pint-logger"

    @property
    def version(self):
        pass
