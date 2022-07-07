from pkgs.web3_tools.config import get_web3
from pkgs.utils import run_multithreader
from datetime import datetime
import calendar
import time

web3 = get_web3()

######
# Timestamp and blockTime functions
######

def str_date_to_timestamp(date_str):
    date_list = [int(x) for x in date_str.split("-")]
    return date_to_timestamp(*date_list)

def timestamp_to_date(timestamp):
    """

    Args:
        timestamp ([int]): [unix timestamp]

    Returns:
        [datetime]: [datetime readable format of the input unix timestamp, must coerce to string after to use]
    """
    date = datetime.utcfromtimestamp(int(timestamp))
    return date

def date_to_timestamp(YYYY,MM,DD,hour=0,minute=0,second=0):
    """

    Args:
        YYYY ([int]): [year]
        MM ([int]): [month]
        DD ([int]): [day]
        minutes (int, optional): [minutes]. Defaults to 0.
        seconds (int, optional): [seconds]. Defaults to 0.

    Returns:
        [int]: [unix timestamp utc]
    """
    date_time = datetime(YYYY, MM, DD, hour, minute, second)
    timestamp = calendar.timegm(date_time.timetuple())
    return timestamp

def get_block(block_number='latest',txs=False):
    """
    Retrieve block details from any existing block from the specified chain.
    Args:
        block_number (str, optional): [description]. Defaults to 'latest'.
        txs (bool, optional): [Include transaction details in the block]. Defaults to False.
        chain (str, optional): [Which blockchain to query]. Defaults to 'eth'.

    Returns:
        [dict]: [block details]
    """
    block = dict(web3.eth.get_block(block_number,txs))
    return block

def get_block_timestamp(block_number):
    return get_block(block_number)['timestamp']

def get_block_from_timestamp(timestamp):
    '''
    Recursive function to obtain block from a timestamp, using a lower and upper limit blocks that shrink with each iteration
    '''
    latest_block = web3.eth.get_block('latest')['number']
    def get_predicted_block_from_timestamp(time_in_seconds, lower_limit_block=1, upper_limit_block=latest_block):
        lower_limit_block = max(1, lower_limit_block)
        upper_limit_block = min(latest_block, upper_limit_block)
        if lower_limit_block <= upper_limit_block <= lower_limit_block+5:
            return lower_limit_block # target block within 5 blocks, can shorted to get more accurate result
        try:
            t0, t1 = get_block(lower_limit_block)['timestamp'], get_block(upper_limit_block)['timestamp']
        except:
            time.sleep(5)
            t0, t1 = get_block(lower_limit_block)['timestamp'], get_block(upper_limit_block-1)['timestamp']
        av_block_time = (t1 - t0) / (upper_limit_block-lower_limit_block)
        # if block-times were evenly-spaced, get expected block number
        evenly_spaced_avg_block_time = (time_in_seconds - t0) / (t1-t0)
        expected_block = int(lower_limit_block + evenly_spaced_avg_block_time * (upper_limit_block - lower_limit_block))
        # get the ACTUAL time for that block
        expected_block_time = get_block(expected_block)['timestamp']
        # use the discrepancy to improve our guess
        est_nblocks_from_expected_to_target = int((time_in_seconds - expected_block_time) / av_block_time)
        expected_target_block = expected_block + est_nblocks_from_expected_to_target
        r = abs(est_nblocks_from_expected_to_target)
        return get_predicted_block_from_timestamp(time_in_seconds, expected_target_block - r, expected_target_block + r)
    predicted_block = get_predicted_block_from_timestamp(timestamp)
    predicted_timestamp = get_block(predicted_block)['timestamp']
    while predicted_timestamp<timestamp:
        predicted_block+=1
        predicted_timestamp = get_block(predicted_block)['timestamp']
    return predicted_block


def get_block_time_multithread(block_list):
    block_list = list(set(block_list))
    timestamps = run_multithreader(get_block_timestamp,block_list)
    return dict(zip(block_list,timestamps))