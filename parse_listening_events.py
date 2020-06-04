import argparse
from pathlib import Path

from tqdm import tqdm
import pandas as pd

TOTAL_LISTENING_EVENTS = 1_088_161_692


def parse(input_file, output_dir, cutoff=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    data = {}
    print('Parsing...')
    with open(input_file) as le_fp:
        for count, line in enumerate(tqdm(le_fp, total=TOTAL_LISTENING_EVENTS)):
            user_id, artist_id, _, track_id, _ = line.split()

            if user_id not in data:
                data[user_id] = {}

            if track_id not in data[user_id]:
                data[user_id][track_id] = {'playcount': 0, 'artist_id': artist_id}
            data[user_id][track_id]['playcount'] += 1

            if cutoff is not None and count >= cutoff:
                break

    print('Saving...')
    for user_id, listens in tqdm(data.items()):
        user_file = output_dir / f'{user_id}.csv'
        df = pd.DataFrame.from_dict(listens, orient='index')
        df.sort_values(by='playcount', ascending=False).to_csv(user_file, index_label='track_id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to LFM-1b_LEs.txt')
    parser.add_argument('output_dir', help='path to output directory')
    parser.add_argument('--cutoff', type=int, help='if specified, will only parse this number of listening events')
    args = parser.parse_args()
    parse(args.input_file, args.output_dir, args.cutoff)
