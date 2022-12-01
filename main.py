import argparse
import json

from utils import AddReservations
from datetime import datetime


def make_reservations_object(reservations):
    dict_reservations = json.loads(reservations)
    for i in dict_reservations:
        start_time = dict_reservations[i]["start_time"]
        end_time = dict_reservations[i]["end_time"]
        dict_reservations[i]["start_time"] = datetime(day=start_time["day"], month=start_time["month"],
                                                      year=start_time["year"], hour=start_time["hour"],
                                                      minute=start_time["minute"])
        dict_reservations[i]["end_time"] = datetime(day=end_time["day"], month=end_time["month"],
                                                    year=end_time["year"], hour=end_time["hour"],
                                                    minute=end_time["minute"])
    return dict_reservations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reservations", required=True, type=str,
                        help="""Json object, which is the list of already made reservations, with the structure. 
(e.g. [{"start_time": {"day":11, "month":1, "year":2022, "hour":5, "minute":0},
        "end_time": {"day":11, "month":1, "year":2022, "hour":5, "minute":30}} ....])""")
    parser.add_argument("--duration", required=True, type=int)

    args = parser.parse_args()
    possible_reservations = sorted(AddReservations(reservations=make_reservations_object(args.reservations),
                                                   duration=args.duration).init_dates(),
                                   key=lambda k: k['start_date'])
    print(possible_reservations)
