import time
from datetime import datetime
import math
import pprint

from data_preparation.data_grouping import load_grouped_filtered_sstubs
from constants import MIN_SSTUB_PERCENTAGE


def find_min_time_interval(timestamps_list, min_sstubs_percentage):
    '''
    :param timestamps_list: list of timestamps from all sstubs in bucket
    :param min_sstubs_percentage: minimum percentage of bugs that must be part of interval
    :return: shortest time interval in which at least the given percentage of time stamps is covered
    '''

    # calculate number of timestamps that must be within interval (ceil always rounds up)
    min_timestamps_amount = int(math.ceil(len(timestamps_list) * min_sstubs_percentage))

    sorted_timestamps = sorted(timestamps_list)
    shortest_interval = 0
    for i in range(len(timestamps_list)):
        first_timestamp_index = i
        last_timestamp_index = first_timestamp_index + min_timestamps_amount

        if last_timestamp_index >= len(sorted_timestamps):
            break

        diffTime = sorted_timestamps[last_timestamp_index] - sorted_timestamps[first_timestamp_index]
        if i == 0 or diffTime.days < shortest_interval:
            shortest_interval = diffTime.days

    return shortest_interval


def get_projects_to_bucket_details():
    data = load_grouped_filtered_sstubs()
    projects_to_buckets_details = dict()

    for project_name, buckets_to_sstubs in data.items():
        projects_to_buckets_details[project_name] = {}  # Create new entry in dict for each project

        for bucket_id, sstubs in buckets_to_sstubs.items():
            bucket_timestamps = []  # reset timestamp list for each bucket

            for sstub in sstubs:
                time = sstub['fixTime']
                time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').date()
                bucket_timestamps.append(time)

            min_time = min(bucket_timestamps)
            max_time = max(bucket_timestamps)
            diff_time = max_time - min_time
            num_of_sstubs = len(sstubs)
            interval = find_min_time_interval(bucket_timestamps, MIN_SSTUB_PERCENTAGE)

            projects_to_buckets_details[project_name][bucket_id] = {'timestamps': bucket_timestamps,
                                                                    'overallDiffTime': diff_time.days,
                                                                    'thresholdDiffTime': interval,
                                                                    'numOfSstubs': num_of_sstubs
                                                                    }

    pprint.pprint(projects_to_buckets_details)
    return projects_to_buckets_details


def main():
    start_time = time.process_time()
    get_projects_to_bucket_details()
    print('')
    print("--- %s seconds ---" % (time.process_time() - start_time))
    print('')


if __name__ == "__main__":
    main()