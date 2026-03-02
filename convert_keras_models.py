"""
Convert TF2-saved .keras (Keras3 zip format) files to standard .h5 using tf_keras.
Patches config.json to replace legacy TF2 module paths, then rebuilds model + loads weights.
Run once: python convert_keras_models.py
"""
import zipfile, json, os, warnings, tempfile
warnings.filterwarnings('ignore')

os.environ['TF_USE_LEGACY_KERAS'] = '0'

import tf_keras as tfk  # type: ignore

KERAS_FILES = [
    'artifacts/models/churn_widedeep_20260218_184733.keras',
    'artifacts/models/recommendation_ncf_20260218_185653.keras',
    'artifacts/models/forecast_lstm_20260220_204816.keras',
    'artifacts/models/sentiment_lstm_20260220_211402.keras',
    'artifacts/models/recommendation_wide_deep_20260218_185653.keras',
    'artifacts/models/churn_tf_widedeep.keras',
    'artifacts/models/churn_tf_transformer.keras',
]

MODULE_MAP = {
    'keras.src.engine.functional':      'keras.engine.functional',
    'keras.src.layers':                  'keras.layers',
    'keras.src.layers.core':             'keras.layers',
    'keras.src.layers.regularization.dropout': 'keras.layers',
    'keras.src.layers.normalization.batch_normalization': 'keras.layers',
    'keras.src.layers.rnn.lstm':         'keras.layers',
    'keras.src.layers.rnn.gru':          'keras.layers',
    'keras.src.layers.embeddings':       'keras.layers',
    'keras.src.layers.merging.add':      'keras.layers',
    'keras.src.layers.merging.concatenate': 'keras.layers',
    'keras.src.layers.reshaping.flatten': 'keras.layers',
    'keras.src.layers.core.dense':       'keras.layers',
    'keras.src.layers.core.activation':  'keras.layers',
    'keras.src.layers.core.input_layer': 'keras.layers',
}

def patch_config(cfg):
    """Recursively patch TF2 module paths and convert batch_input_shape -> shape."""
    if isinstance(cfg, dict):
        mod = cfg.get('module', '')
        if mod in MODULE_MAP:
            cfg['module'] = MODULE_MAP[mod]
        elif mod.startswith('keras.src.'):
            cfg['module'] = mod.replace('keras.src.', 'keras.')

        sub = cfg.get('config', {})
        if isinstance(sub, dict):
            # Convert batch_input_shape=[None, N] -> shape=[N] (drop batch dim)
            if 'batch_input_shape' in sub:
                bis = sub.pop('batch_input_shape')
                if isinstance(bis, (list, tuple)) and len(bis) > 1:
                    sub['shape'] = list(bis[1:])
                elif isinstance(bis, (list, tuple)) and len(bis) == 1:
                    sub['shape'] = []
            # Remove other incompatible keys
            sub.pop('input_length', None)
            sub.pop('time_major', None)
            sub.pop('shared_object_id', None)
            # BatchNorm axis: if list wrap -> unwrap to int
            if 'axis' in sub and isinstance(sub['axis'], list) and len(sub['axis']) == 1:
                sub['axis'] = sub['axis'][0]

        for v in list(cfg.values()):
            patch_config(v)
    elif isinstance(cfg, list):
        for item in cfg:
            patch_config(item)
    return cfg


for src in KERAS_FILES:
    out = src.replace('.keras', '_compat.h5')
    if not os.path.exists(src):
        print(f'SKIP {src} (not found)')
        continue
    if os.path.exists(out):
        print(f'EXISTS {os.path.basename(out)}')
        continue
    try:
        with zipfile.ZipFile(src, 'r') as z:
            cfg = json.loads(z.read('config.json'))
            weights_data = z.read('model.weights.h5')

        patched = patch_config(cfg)

        # Build model from patched JSON config
        model = tfk.models.model_from_json(json.dumps(patched))

        # Write weights to temp file and load
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp:
            tmp.write(weights_data)
            tmp_path = tmp.name

        model.load_weights(tmp_path)
        os.unlink(tmp_path)

        # Save as proper HDF5
        model.save(out)
        print(f'OK  {os.path.basename(out)} -> {type(model).__name__}')
    except Exception as e:
        print(f'ERR {os.path.basename(src)}: {e}')
