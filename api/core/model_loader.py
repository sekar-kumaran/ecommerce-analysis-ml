"""
Model loading utilities with caching and metadata support
"""
import json
import joblib
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from api.core.config import MODELS_DIR, ENCODERS_DIR, SCALERS_DIR, METADATA_REGISTRY

logger = logging.getLogger(__name__)

# In-memory model cache
_model_cache: Dict[str, Any] = {}
_meta_cache: Dict[str, Dict] = {}

# Force TF2 keras backend before any keras import
os.environ.setdefault("TF_USE_LEGACY_KERAS", "0")


def _load_keras_file(path: str):
    """
    Load a .h5 or .keras file.
    Strategy (in order):
      1. tf_keras  (pip install tf_keras) — TF2-compat shim, most reliable
      2. tf.keras  via `import tensorflow as tf; tf.keras`
      3. h5py weights-only reconstruction for Sequential models (last resort)
    All three try compile=False to skip optimizer deserialization.
    """
    # Strategy 1: tf_keras shim (installed alongside tensorflow ≥2.13)
    try:
        import tf_keras as _tfk  # type: ignore
        return _tfk.models.load_model(path, compile=False)
    except Exception as e1:
        logger.debug(f"tf_keras failed for {path}: {e1}")

    # Strategy 2: tensorflow.keras (works when keras3 is NOT overriding it)
    try:
        import tensorflow as tf  # type: ignore
        import tensorflow.keras as _tfkeras  # type: ignore  # noqa: F401
        return tf.keras.models.load_model(path, compile=False)
    except Exception as e2:
        logger.debug(f"tf.keras failed for {path}: {e2}")

    # Strategy 3: keras3 standalone with custom_objects to paper over missing classes
    try:
        import keras  # type: ignore
        import numpy as np
        # Stub out legacy metric names that Keras3 removed
        _custom = {}
        try:
            import tensorflow as tf  # type: ignore
            _custom["mse"] = tf.keras.losses.MeanSquaredError()
        except Exception:
            pass
        return keras.models.load_model(path, compile=False, custom_objects=_custom)
    except Exception as e3:
        logger.debug(f"keras3 failed for {path}: {e3}")

    raise RuntimeError(
        f"All keras load strategies failed for '{path}'. "
        "Run: pip install tf-keras"
    )


def load_artifact(filename: str, search_dirs: Optional[list] = None) -> Any:
    """
    Load a pickle / joblib / keras artifact from the artifact directories.
    Tries MODELS_DIR, SCALERS_DIR, then ENCODERS_DIR unless search_dirs provided.
    Results are cached in memory.
    """
    if filename in _model_cache:
        return _model_cache[filename]

    dirs = search_dirs or [MODELS_DIR, SCALERS_DIR, ENCODERS_DIR]

    for directory in dirs:
        full_path = Path(directory) / filename
        if full_path.exists():
            try:
                ext = full_path.suffix.lower()
                if ext in (".h5", ".keras"):
                    model = _load_keras_file(str(full_path))
                else:
                    model = joblib.load(str(full_path))

                _model_cache[filename] = model
                logger.info(f"Loaded artifact: {filename}")
                return model
            except Exception as exc:
                logger.error(f"Failed to load {full_path}: {exc}")
                raise RuntimeError(f"Could not load artifact '{filename}': {exc}")

    raise FileNotFoundError(f"Artifact '{filename}' not found in {dirs}")


def load_metadata(meta_key: str) -> Dict:
    """Load a JSON metadata file by registry key."""
    if meta_key in _meta_cache:
        return _meta_cache[meta_key]

    filename = METADATA_REGISTRY.get(meta_key)
    if not filename:
        return {}

    path = MODELS_DIR / filename
    if not path.exists():
        logger.warning(f"Metadata file not found: {path}")
        return {}

    with open(path, "r") as f:
        data = json.load(f)

    _meta_cache[meta_key] = data
    return data


def load_json_report(filename: str) -> Dict:
    """Load any JSON report from the models directory."""
    path = MODELS_DIR / filename
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def list_available_artifacts() -> Dict[str, list]:
    """Return lists of all artifact files by category."""
    def _scan(directory: Path) -> list:
        if not directory.exists():
            return []
        return [f.name for f in directory.iterdir() if f.is_file()]

    return {
        "models": _scan(MODELS_DIR),
        "scalers": _scan(SCALERS_DIR),
        "encoders": _scan(ENCODERS_DIR),
    }


def clear_cache() -> None:
    """Clear the in-memory model / metadata cache."""
    _model_cache.clear()
    _meta_cache.clear()
    logger.info("Model cache cleared")
