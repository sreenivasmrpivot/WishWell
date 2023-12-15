# Set up conda environment for wishwell
conda create -n wishwell python=3.10 # required for all dependencies to work as expected.
conda activate wishwell
python3 --version
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Cleanup conda environment for wishwell
conda deactivate
conda env remove --name wishwell    
