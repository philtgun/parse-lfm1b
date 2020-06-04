# parse-lfm1b
Some scripts to parse [LFM-1b](http://www.cp.jku.at/datasets/LFM-1b/) dataset

Requires Python 3.7+

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Calculate top tracks per user

```bash
python parse_listening_events path/to/LFM-1b_LEs.txt path/to/output_dir --cutoff=1000000
```
