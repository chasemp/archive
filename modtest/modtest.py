import sys
import random
try_match = []
tries = 10
#make 10 passes of user defined range
while tries > 0:
    match = []
    #how many times should I try to match my modulus op
    for i in range(0, int(sys.argv[1])):
        if random.randint(0, 100) % 10 == 0:
            match.append(i)

    #append the number of matches
    try_match.append(len(match))
    tries -= 1

average_sampled = sum(try_match) / 10
print average_sampled * 100 / int(sys.argv[1]) 
