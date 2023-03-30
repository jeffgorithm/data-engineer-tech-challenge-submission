cd ~/data-pipelines

source venv/bin/activate

python main.py \
--input_dir datasets/ \
--success_dir output/success \
--unsuccessful_dir output/unsuccessful