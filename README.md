# parse-lfm1b
Some scripts to parse [LFM-1b](http://www.cp.jku.at/datasets/LFM-1b/) dataset

Requires Python 3.7+

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Calculate top tracks per user

With the batch size of 250,000,000 (around 12GB of memory usage)

```bash
python parse_listening_events path/to/LFM-1b_LEs.txt path/to/output_dir_1 --cutoff=250000000
python parse_listening_events path/to/LFM-1b_LEs.txt path/to/output_dir_2 --skip=250000000 --cutoff=500000000
python parse_listening_events path/to/LFM-1b_LEs.txt path/to/output_dir_3 --skip=500000000 --cutoff=750000000
python parse_listening_events path/to/LFM-1b_LEs.txt path/to/output_dir_4 --skip=750000000
python merge_listening_events path/to/output_dir_all path/to/output_dir_1 path/to/output_dir_2 path/to/output_dir_3 path/to/output_dir_4
```
