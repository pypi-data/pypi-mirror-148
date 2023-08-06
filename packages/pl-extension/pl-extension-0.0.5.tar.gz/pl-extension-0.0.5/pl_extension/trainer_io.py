"""
pl trainer io.
"""

from pl_extension.callbacks import ModelCheckpoint

import pytorch_lightning as pl

__all__ = ["get_checkpoint_dirpath"]


def get_checkpoint_dirpath(trainer: pl.Trainer) -> str:
    """
    return checkpoint dirpath.
    """
    ck_callbacks = [
        c for c in trainer.callbacks if isinstance(c, ModelCheckpoint)
    ]
    assert len(ck_callbacks) > 0
    return ck_callbacks[0].dirpath
