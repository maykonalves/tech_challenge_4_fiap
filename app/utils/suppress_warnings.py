import os
import logging

def suppress_tensorflow_warnings():
    """
    Suppresses TensorFlow warnings and forces CPU-only mode.
    """
    # Disable TensorFlow logging except for errors
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0=all, 1=info, 2=warning, 3=error
    
    # Force TensorFlow to use CPU only
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("TensorFlow configured to run on CPU only. GPU warnings suppressed.")
