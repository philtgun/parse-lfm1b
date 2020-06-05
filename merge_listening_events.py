import argparse
from pathlib import Path
import shutil

from tqdm import tqdm
import pandas as pd


def parse(input_dirs, output_dir):
    data = {}
    for input_dir in input_dirs:
        user_files = sorted(Path(input_dir).rglob('*.csv'))
        for user_file in user_files:
            user_id = int(user_file.stem)
            if user_id not in data:
                data[user_id] = []
            data[user_id].append(input_dir)

    Path(output_dir).mkdir(exist_ok=True)
    merged_users = []
    for user_id, input_dirs in tqdm(data.items()):
        if len(input_dirs) == 1:
            shutil.copy(str(Path(input_dirs[0]) / f'{user_id}.csv'), output_dir)
        else:
            dfs = [pd.read_csv(Path(input_dir) / f'{user_id}.csv', index_col='track_id') for input_dir in input_dirs]
            df = pd.concat(dfs).groupby(by=['track_id', 'artist_id']).sum().sort_values(by='playcount', ascending=False)
            df.reset_index(level=['artist_id'], inplace=True)
            df[['playcount', 'artist_id']].to_csv(Path(output_dir) / f'{user_id}.csv')
            merged_users.append(user_id)
    print(f'Merged users: {len(merged_users)}')
    print(merged_users)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', help='path to output directory')
    parser.add_argument('input_dirs', nargs='+', help='list of paths to directories to merge')
    args = parser.parse_args()
    parse(args.input_dirs, args.output_dir)
