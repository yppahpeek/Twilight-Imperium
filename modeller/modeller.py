import random

# """Fleet Class contains a list of all the units each force has."""

class Fleet():
    def __init__(self, units):
        # Takes list of strs and, for every valid unit.type, creates a new Unit in the Fleet 
        self.units = units
                            
    def number_of_hits(self):
        hits = 0
        for unit in self.units:
            
            if unit.type == "ws":
                n_rolls = 3
            else:
                n_rolls = 1
            
            # this takes into acount multiple rolls from ws (and flagship when they get added)
            while n_rolls > 0:
                roll = round(random.random(), 1)

                if roll <= unit.hit:
                    hits += 1
                
                n_rolls -= 1
            
        return hits
    
    def assign_hits(self, dmg):
        while dmg > 0:
            
            for unit in self.units:
                # take a hit point
                unit.hp -= 1
                
                # remove unit from the fleet if it has 0 hit points
                if unit.hp == 0:
                    self.units.remove(unit)
                
                dmg -= 1
            return  
    
    
    # Getter for units[]
    @property
    def units(self):
        return self._units
    
    # Setter for units[]
    @units.setter
    def units(self, unit_list):
        units = []
        # TODO - add exceptions/error checking here for invalid units
        for u in unit_list:
            try:
                unit = Unit(u)
                units.append(unit)
            except:
                continue
        
        self._units = units    
    
    # Getter for total_hp
    @property
    def total_hp(self):
        total_hp = 0
        for u in self.units:
            total_hp += u.hp
        return total_hp
    
    # Getter for total_sustain - this is needed so that we can quickly determine if sustain damage is needed
    @property
    def total_sustain(self):
        total_sustain = 0
        for u in self.units:
            total_sustain += u.sustain
            
        return total_sustain

                
"""Unit class contains all the details for each unit type. User must specify which type of unit they want to add to their fleet when they instantiate that unit. For example, unit = Unit('Carrier') - this will be handled with the command line args"""

class Unit():
    def __init__(self, type):
        # Error handling for incorrect unit types.
        # Units must be in ["car", "cru", "des", "dre", "fig", "ws"]
        if type not in ["car", "cru", "des", "dre", "fig", "ws"]:
            raise ValueError("Unit type must be in ['car', 'cru', 'des', 'dre', 'fig', 'ws']")
       
        self.type = type
        
        # takes account of sustain damage. This will be >0 for "dre" or "ws" type units
        self.sustain = 0
        
        # set HP for units. Only Dreadnoughts and War Suns have sustain damage.
        if type in ["dre", "ws"]:
            # dre and ws type ships have 2 hp and 1 sustain. The 1 sustain is only used as a counter, sustain damage happens to hp
            self.hp = 2
            self.sustain = 1
        else: 
            self.hp = 1
            
        # set hit chance for units.
        # Carriers, Destroyers and Fighters hit on 9.
        if type in ["car", "des", "fig"]:
            self.hit = 0.1
       # Cruisers hit on 7.
        elif type == "cru":
            self.hit = 0.3
        # Dreadnoughts hit on 5.
        elif type == "dre":
            self.hit = 0.5
        # War Suns hit on 3 * 3. The multiplier will be factored in later on. 
        else:
            self.hit = 0.7
        
        # set movement. Cruisers, Destroyers and War Suns move 2. All other level 1 ships move 1.
        if type in ["cru", "des", "ws"]:
            self.mov = 2
        else:
            self.mov = 1
            
        self.capacity = 4

    def __str__(self):
        if self.type == "ws":
            return f"{self.type} unit has movement of {self.mov}, {self.hp} HP and 3 * {self.hit} chance of hit"
        else:
            return f"{self.type} unit has movement of {self.mov}, {self.hp} HP and a {self.hit} chance of hit"
        
        
def main():
    number_of_scraps = 10000
    
    # get input strs on each of the fleets taking part in the scrap
    att_fleet = input("Attacking units").split()
    def_fleet = input("Defending units"). split()
    
    # dict to track winners, losers and draws
    outcomes = {"Attacker": 0, "Defender": 0, "Draw": 0}
    
    # scrap number_of_scraps times
    while number_of_scraps > 0:
        # copy master fleets which can have items removed
        scrap_att_fleet = Fleet(att_fleet)
        scrap_def_fleet = Fleet(def_fleet)
        
        # add 1 onto the attacker, defender or draw tracker
        outcomes[scrap(scrap_att_fleet, scrap_def_fleet)] += 1
        
        # remove 1 from number_of_scraps
        number_of_scraps -= 1
        
    print(outcomes)
    

"""Function iterates for NUMBER_OF_SCRAPS, and simulates and records the outcome of a whole scrap. Input are two fleet lists of Units, which privide fleet hits and take damage."""
def scrap(att_fleet, def_fleet):
    
    while att_fleet.total_hp > 0 and def_fleet.total_hp >0:
        att_hits = att_fleet.number_of_hits()
        def_hits = def_fleet.number_of_hits()

        take_damage(att_fleet, def_hits)
        take_damage(def_fleet, att_hits)
        
    if att_fleet.total_hp == 0 and def_fleet.total_hp == 0:
        return "Draw"
    elif att_fleet.total_hp == 0:
        return "Defender"
    else:
        return "Attacker"    
    
    
# function makes sure sustain hits are applied first, then hits for the rest of the fleet
def take_damage(f, h):
    # sustain damage comes first
    if f.total_sustain > 0:
        sustain_damage(f, h)
       
        # TODO - for debugging. Find out why att_fleet is more likely to win the def_fleet in an equal battle
        print(f.total_hp, "HP and ", f.total_sustain, " total sustain")
        
    # once sustain hits are dealt, start removing ships
    hit_point_damage(f, h)
    
    return
        
        
# damages only
def sustain_damage(f, h):
    
    for unit in f.units:
        # if no more hits, h, return before dealing more damage
        if h == 0:
            return
            
        # only deal damage is a unit has sustain damage (ie more than 1 hit)
        if unit.hp > 1:
            unit.hp -= 1
            # also reduce the sustain for the fleet so that this function can be skipped later
            unit.sustain -= 1
            h -= 1        
               
               
# assigns hits to units
def hit_point_damage(f, h):
    
    # similar structure to sustain_damage()
    for unit in f.units:
        
        # if no more hits, h, available, then return from function
        if h == 0:
            return
        
        # if unit is dead, skip over it onto the next one
        if unit.hp == 0:
            continue
        
        unit.hp -= 1
        h -= 1
        
if __name__ == "__main__":
    main()