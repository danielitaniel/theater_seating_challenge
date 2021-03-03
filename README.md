# Theater Seating Challenge

In this project, I use create an algorithm utilizing binary search in order to seat movie watchers at a theater (with COVID-19 protocols).

# Requirements:

Python 3.8

# COVID-19 Protocols

Due to the ongoing pandemic, movie theaters have restrictions. Rather than having a capacity, this algorithm assumes that parties be seperated by at least three empty seats and/or an entire row.

# Assumptions

- In order for inputs to be read properly, there can only be one new line at the end of an input.txt file. Otherwise, functionality will be broken.

- This algorithm assumes that movie watchers prefer to be seated in the middle aisle and middle seat of the theater based on statistical research by the developer.


# The Process

The user starts execution of the program by running `python main.py`, in which they will immediately be prompted with a command asking them to enter the relative path in which to read the input .txt file from. If the path is valid, the program will create an output file and will return the relative path to the output file on the command line. Otherwise, the user will be thrown with an `Error` message.

# The Algorithm

The algorithm has 7 main steps:

1. First come first serve. Early birds are seated in the middle aisle and middle seat of the theater. 
2. To ensure customer satisfaction, this algorithm attempts to keep parties as clustered together as possible (even during a pandemic!). There are two such cases for this: a). The party consists of a size less than 21. In this cass all customers can sit together. b). The party consists of a size greater than 20. In this case, the algorithm will split the party into partitions, where each partition is roughly the same size. These partitions will all sit together. In the case where all but one partition can be seated, the reservation will not go through and there will NOT be a booking.
3. The algorithm will continue to assign customers in the middle seats (regardless of row) until all center seats have been taken
4. At this point, the algorithm will switch and utilize binary search. The algorithm first searches for empty seats to the left of where the center audience is seated.
5. If #3 fails, then the binary search will search to the right of the center of the audience.
6. If #2, #3, and #4 fail, then we revert to a brute force approach, in order to achieve customer satisfaction as there may be available seats even with the social distancing restrictions.
7. If #2-#5 fail. then there is no such possible arrangement for the party. At this time, no booking will be made

# The Input

The input should be a .txt file. It's structure should be as follows:

`
R001 3
R002 2
R003 5
.... .
.... .
R### #
`


Where R### represents the reservation, and the # to the right represents the number of seats requested for the corresponding reservation.

# The Output

The output is guaranteed to be a .txt file. It's structure will be as follows:

`
R001 F9, F10, F11
R002 H9, H10
R003 D8, D9, D10, D11, D12
.... .
.... ..
R### booking unavailable
`

