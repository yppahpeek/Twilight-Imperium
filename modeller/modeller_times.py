import modeller
import timeit


# create fleets for use in timetit() function - no need for user input
att_fleet = modeller.Fleet("dre dre dre")
def_fleet = modeller.Fleet("dre cru dre")

print(att_fleet)
print(def_fleet)

# t = timeit.timeit(stmt="[scrap(att_fleet, def_fleet)]", setup="from modeller import scrap, Fleet, Unit", number = 10000)

# print(t)