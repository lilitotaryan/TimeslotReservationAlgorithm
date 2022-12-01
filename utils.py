from datetime import datetime, timedelta
import numpy


class AddReservations:

    def __init__(self, reservations, duration=30):
        matrix = numpy.zeros((48, 48))
        # create array and keep only start_times
        for i in reservations:
            matrix[self.time_to_int(i.get("start_time"))][self.time_to_int(i.get("end_time"))] = 1
        self.matrix = matrix
        self.duration = duration

    @staticmethod
    def time_to_int(time):
        compare_date = datetime(year=time.year, month=time.month, day=time.day, hour=0, minute=0).timestamp()
        time = time.timestamp()
        return int((time - compare_date) // (60 * 30))

    @staticmethod
    def int_to_time(int_minutes):
        return (datetime(year=2020, month=11, day=9, hour=0, minute=0) + timedelta(minutes=int_minutes * 30)).time()

    def init_dates(self):
        result = []
        i = 0
        while i <= 48 - self.duration // 30:
            # if no 1 from i to i+self duration or if not end_date and next_start_date in i to i+self duration
            # i.g end_date is between i and i+self_duration and next_start_date is between i and i+self_duration
            if numpy.amax(self.matrix[i:i + self.duration // 30]) == 0:
                result.append({"start_date": self.int_to_time(i),
                               "end_date": self.int_to_time(i + self.duration // 30)})
                i = i + self.duration // 30
            else:
                # create new array that has values of the start_date and next start_date or arrange
                # array in the reversed order and keep values of previous nodes
                result_where = numpy.where(self.matrix[i:i + self.duration // 30] == 1)
                i = int(list(zip(result_where[0], result_where[1]))[0][1])
        return result


# todo check this
class AddReservationsOptimized:

    def __init__(self, reservations, duration=30):
        array_one = numpy.zeros(48)
        # array should be array of tuples
        array_two = numpy.zeros(len(reservations))
        # create array and keep only start_times
        for i in range(0, len(reservations)):
            array_one[self.time_to_int(reservations[i].get("start_time"))] = \
                self.time_to_int(reservations[i].get("end_date"))
            array_two[i] = self.time_to_int(reservations[i + 1].start_time) if reservations[i + 1] else None
        self.array_one = array_one
        self.array_two = array_two
        self.reservations = reservations
        self.duration = duration

    @staticmethod
    def time_to_int(time):
        compare_date = datetime(year=time.year, month=time.month, day=time.day, hour=0, minute=0).timestamp()
        time = time.timestamp()
        return int((time - compare_date) // (60 * 30))

    @staticmethod
    def int_to_time(int):
        return (datetime(year=2020, month=11, day=9, hour=0, minute=0) + timedelta(minutes=int * 30)).time()

    def init_dates(self):
        result = []
        i = 0
        arr_two_i = 0
        while i <= 48 - self.duration // 30:
            # if no 1 from i to i+self duration or if not end_date and next_start_date in i to i+self duration
            # i.g end_date is between i and i+self_duration and next_start_date is between i and i+self_duration
            if not (i < self.array_one[i] < i + self.duration // 30 and
                    i < self.array_two[arr_two_i] < i + self.duration // 30):
                result.append({"start_date": self.int_to_time(i),
                               "end_date": self.int_to_time(i + self.duration // 30)})
                i = i + self.duration // 30
            else:
                # create new array that has values of the start_date and next start_date or arrange
                # array in the reversed order and keep values of previous nodes
                i = self.array_two[arr_two_i]
                arr_two_i += 1
        return result
