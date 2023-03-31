cd ~/data-pipelines

source venv/bin/activate

python src/main.py \
--input_dir input/ \
--success_dir output/success \
--unsuccessful_dir output/unsuccessful