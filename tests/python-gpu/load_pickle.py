'''Loading a pickled model generated by test_pickling.py, only used by
`test_gpu_with_dask.py`'''
import unittest
import os
import xgboost as xgb
import json

from test_gpu_pickling import build_dataset, model_path, load_pickle


class TestLoadPickle(unittest.TestCase):
    def test_load_pkl(self):
        '''Test whether prediction is correct.'''
        assert os.environ['CUDA_VISIBLE_DEVICES'] == '-1'
        bst = load_pickle(model_path)
        x, y = build_dataset()
        test_x = xgb.DMatrix(x)
        res = bst.predict(test_x)
        assert len(res) == 10

    def test_predictor_type_is_auto(self):
        '''Under invalid CUDA_VISIBLE_DEVICES, predictor should be set to
        auto'''
        assert os.environ['CUDA_VISIBLE_DEVICES'] == '-1'
        bst = load_pickle(model_path)
        config = bst.save_config()
        config = json.loads(config)
        assert config['learner']['gradient_booster']['gbtree_train_param'][
            'predictor'] == 'auto'

    def test_predictor_type_is_gpu(self):
        '''When CUDA_VISIBLE_DEVICES is not specified, keep using
        `gpu_predictor`'''
        assert 'CUDA_VISIBLE_DEVICES' not in os.environ.keys()
        bst = load_pickle(model_path)
        config = bst.save_config()
        config = json.loads(config)
        assert config['learner']['gradient_booster']['gbtree_train_param'][
            'predictor'] == 'gpu_predictor'
