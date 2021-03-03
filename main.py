import copy
from math import ceil
import sys



"""
NOTE: As of 03/03/21 this COVID-19 Movie Theater Seating Protocol is fully
functionable... though this could definitely use refactoring.

TODO: Look in to using coroutines to allow for asynchronous programming
"""

ROW_NUMBER_TO_LETTER = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J"
}



class MovieTheaterSeating:

    num_rows = 10
    num_columns = 20



    def __init__(self, fp):
        self.file_path = fp
        self.theater_seats = self.initialize_movie_theater()
        self.reservations = self.get_input_rows()
        self.popular_rows = [5, 7, 3, 9, 1]
        self.seats_remaining_per_row = [0,20]*5


    """
    Create 10x20 matrix where rows alternate between containing all 1's or
    all 0's.

    A 0 denotes that the seat is unavailable for use
    A 1 denotes that the seat is available for usw
    """

    def initialize_movie_theater(self):
        empty_row = [1]*self.num_columns
        excluded_seats = [0]*self.num_columns
        theater = []
        for i in range(10):
            if(i%2 ==0):
                theater.append(excluded_seats)
            else:
                theater.append(empty_row)
        return theater



    """
    Open and read from 'fn' and convert the input txt to an array consisting
    of each reservation.
    """

    def get_input_rows(self):
        try:
            f = open(self.file_path, "r")
            input = f.read()
            input_array = input.split('\n')
            f.close()
            return input_array[:-1]
        
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise



    """
    Search whether or not a certain number of seats (coming from a reservation)
    is possible.

    If possible; return a list consisting of [row, column] tuples.

    Otherwise; this function will return an empty list.
    """

    def search_available_row_seats(self, row, num_seats):
        left = 0
        right = self.num_columns - 1

        seats_remaining = num_seats

        left_side_checked = False

        right_side_checked = False

        while((left <= right) or (not left_side_checked) or (not right_side_checked)):
            # mid represents the middle seat number relative to the group
            if (not left_side_checked):
                mid = max(0,((right + left) // 2) - (num_seats // 2) - 1)
            else:
                mid = ((right + left) // 2)

            if(mid < 0):
                mid = 0
            seats_booked = []


            if (self.theater_seats[row][mid]):
                potential_seat_column = mid
                enough_seats = True
                if (mid + num_seats >= self.num_columns):
                    return seats_booked
                for seat in self.theater_seats[row][mid:mid+num_seats]:
                    if(seat == 0):
                        enough_seats = False
                if (enough_seats):
                    j = mid

                    while (j < mid + num_seats):
                        r = copy.deepcopy(self.theater_seats[row])
                        r[j] = 0
                        self.theater_seats[row] = r
                        seats_booked.append([row, j])
                        j+=1

                    j = mid+num_seats
                    while((j < mid+num_seats+3) and (0 < j) and (j < self.num_columns)):
                        r = copy.deepcopy(self.theater_seats[row])
                        r[j] = 0
                        self.theater_seats[row] = r
                        j+=1

                    j = mid - 1
                    while((j > mid - 1 - 3) and (0 <= j) and (j < self.num_columns)):
                        r = copy.deepcopy(self.theater_seats[row])
                        r[j] = 0
                        self.theater_seats[row] = r
                        j-=1

                    return seats_booked
                else:
                    if (not left_side_checked):
                        right = self.num_columns - 1
                        left = ((right) // 2) + (num_seats // 2)
                        left_side_checked = True

                if(left == right):
                    if (not left_side_checked):
                        right = self.num_columns - 1
                        left = ((right) // 2) + (num_seats // 2)
                        left_side_checked = True


            elif ((not left_side_checked) and (right > 0)):
                right = mid - 1
            else:
                if (not left_side_checked):
                    right = self.num_columns - 1
                    left = ((right) // 2) + (num_seats // 2)
                    left_side_checked = True
                elif ((not right_side_checked) and (left < right)):
                    left = mid + 1
                else:
                    right_side_checked = True
                    left = left + 1

        return seats_booked



    """
    Finds an available row to potentially fufill a reservationself.

    This function sets up parameters for search_available_row_seats().

    If, in the case of a reservation containing 20+ people, this function will
    partition the group size into 'roughly' equally sized groups.
    """

    def assign_group_seats(self, num_seats):

        if (sum(self.seats_remaining_per_row) < num_seats):
            return []

        if self.popular_rows == []:
            self.popular_rows = [5, 7, 3, 9, 1]
            row = self.popular_rows[0]

        i = 0
        row = self.popular_rows[0]
        is_too_big = True

        while((i < len(self.popular_rows) - 1) and
            (num_seats > self.seats_remaining_per_row[row])):
                i+=1
                row = self.popular_rows[i]
        if (num_seats <= self.seats_remaining_per_row[row]):
            is_too_big = False

        seats = []

        if(is_too_big):
            partitions = int(ceil(float(num_seats)/20)) # TODO: Fix partitioning
            partition_size = num_seats//partitions
            remaining_members = num_seats % partition_size
            old_theater_copy = copy.deepcopy(self.theater_seats)
            old_remaining_copy = copy.deepcopy(self.seats_remaining_per_row)
            old_popular_rows = copy.deepcopy(self.popular_rows)

            partition = 0
            while(partition<partitions):
                if (partition == partitions - 1):
                    group = self.assign_group_seats(partition_size + remaining_members)
                    if group == []:
                        self.theater_seats = old_theater_copy
                        self.seats_remaining_per_row = old_remaining_copy
                        self.populiar_rows = old_popular_rows
                        seats = []
                        break
                    seats += group
                else:
                    group = self.assign_group_seats(partition_size)
                    if group == []:
                        self.theater_seats = old_theater_copy
                        self.seats_remaining_per_row = old_remaining_copy
                        self.popular_rows = old_popular_rows
                        seats = []
                        break
                    seats += group
                partition +=1



        if (not is_too_big):
            seats = self.search_available_row_seats(row, num_seats)
            if (len(seats) > 0):
                self.seats_remaining_per_row[row] -= len(seats)
                self.popular_rows.pop(i)
        return seats



    """
    In the worst case, after there are a certain amount of reservations/people,
    there is a slight chance a person can fit in the theater by brute forcing
    for a seat
    """
    def brute_force_search(self, num_seats):
        seats_booked = []
        for row in self.popular_rows:
            col = 0
            while (col < self.num_columns):
                enough_seats = True
                if(col + num_seats > self.num_columns):
                    break
                for seat in self.theater_seats[row][col:col+num_seats]:
                    if(seat == 0):
                        enough_seats = False

                if (enough_seats):
                    i = col
                    while (i < col + num_seats):
                        r = copy.deepcopy(self.theater_seats[row])
                        r[i] = 0
                        self.theater_seats[row] = r
                        seats_booked.append([row, i])
                        i+=1
                    return seats_booked
                col+=1
        return seats_booked



"""
This is where execution begins. The user is asked to input a relative or
absolute path via the command line. The user will then
"""
if __name__ == "__main__":
    print("")

    print("Hello! Welcome to the COVID-19 Theater Seating Aranger")

    print("")

    q1 = "Please insert the relative path: "

    file_path = input(q1)

    print(file_path)
    fn = file_path.split("/")[-1]
    outout_path = "outputs/output_" + fn
    
    try:
        output = open(outout_path, "w")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    theater_obj = MovieTheaterSeating(file_path)
    lines = []
    for reservation in theater_obj.reservations:
        reservation_tuple = reservation.split(' ')
        reservation_reference = reservation_tuple[0]
        try:
            num_requested_seats = int(reservation_tuple[1])
        except ValueError as e:
            print("")
            print("Error: For the number of reservations, please input a valid number ")
            print("")
            raise(e)

        booked_seats = theater_obj.assign_group_seats(num_requested_seats)

        start = True

        if booked_seats == []:
            booked_seats = (
                theater_obj.brute_force_search(num_requested_seats)
            )
            if booked_seats == []:
                lines.append(reservation_reference + " booking unavailable")

        for booked_seat in booked_seats:
            row_in_letter_form = ROW_NUMBER_TO_LETTER[booked_seat[0]]
            if start:
                lines.append(reservation_reference + ' ' + (
                    row_in_letter_form + str(booked_seat[1] + 1)
                ))
                start = False
            else:
                lines.append(", " + row_in_letter_form + str(booked_seat[1] + 1))

        lines.append("\n")

    output.writelines(lines)
    output.close()
    print("")

    print("Success! If you would like to check the output, the path is:")

    print("")

    print(outout_path)
