import argparse
from pathlib import Path

from tqdm import tqdm
import pandas as pd

TOTAL_LISTENING_EVENTS = 1_088_161_692


def parse_listening_events(input_file, output_dir, skip=0, cutoff=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # build dictionary of {user_id: {track_id: [playcount, artist_id]}}
    data = {}
    total = (cutoff or TOTAL_LISTENING_EVENTS) - skip
    with open(input_file) as le_fp:
        if skip > 0:
            for _ in tqdm(range(skip), desc='Skipping'):
                next(le_fp)

        for count, line in enumerate(tqdm(le_fp, total=total, desc='Parsing')):
            user_id, artist_id, _, track_id, _ = line.split()
            user_id = int(user_id)
            artist_id = int(artist_id)
            track_id = int(track_id)

            if user_id not in data:
                data[user_id] = {}

            if track_id not in data[user_id]:
                data[user_id][track_id] = [0, artist_id]
            data[user_id][track_id][0] += 1

            if cutoff is not None and count >= total:
                break

    # write CSV files for each user sorted by playcounts descending
    for user_id, listens in tqdm(data.items(), desc='Saving'):
        user_file = output_dir / f'{user_id}.csv'
        df = pd.DataFrame.from_dict(listens, orient='index', columns=['playcount', 'artist_id'])
        df.sort_values(by='playcount', ascending=False).to_csv(user_file, index_label='track_id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to LFM-1b_LEs.txt')
    parser.add_argument('output_dir', help='path to output directory')
    parser.add_argument('--skip', type=int, default=0, help='if specified, will skip this number of listening events')
    parser.add_argument('--cutoff', type=int, help='if specified, will stop at this number of listening events')
    args = parser.parse_args()
    parse_listening_events(args.input_file, args.output_dir, args.skip, args.cutoff)
