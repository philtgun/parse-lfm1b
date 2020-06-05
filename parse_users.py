import argparse

import pandas as pd


def parse_users(input_file, output_file):
    users = pd.read_csv(input_file, delimiter='\t')
    print(f'Total users: {len(users)}')

    users_with_age = users[users['age'] > 0]
    print(f'Total users with age: {len(users_with_age)}')

    users_with_age[['user_id', 'age']].to_csv(output_file, index=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to LFM-1b_users.txt')
    parser.add_argument('output_file', help='path to output csv file')
    args = parser.parse_args()
    parse_users(args.input_file, args.output_file)
