

def init_deps():
    os.system("pip install nemo_toolkit['all']")
    os.system('git clone https://github.com/NVIDIA/apex')
    os.system('cd apex')
    os.system('pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" --global-option="--fast_layer_norm" ./')
    os.system('cd ..')
    print("All depenndencies installed")