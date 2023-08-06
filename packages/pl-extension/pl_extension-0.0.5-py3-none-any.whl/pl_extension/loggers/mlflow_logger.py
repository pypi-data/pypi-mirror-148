import os

from pytorch_lightning.loggers import MLFlowLogger as _MLFlowLogger

__all__ = ["MLFlowLogger"]


class MLFlowLogger(_MLFlowLogger):

    """Custom run_id for MLFlowLogger, required by AIDI."""

    @property
    def run_id(self):
        _ = self.experiment
        _run_id = os.environ.get("MLFLOW_RUN_ID", self._run_id)
        return _run_id
