# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 15:59:11 2017

@author: gawn
"""

# generate overall world
import os
import sys
import time
import numpy
import random
from shutil import rmtree
from pymclevel import mclevel, box, Entity, nbt
from pymclevel.materials import alphaMaterials as m

# let's try without this at the moment
#from tree import Tree, treeObjs

# Where does the world file go?
worlddir = sys.argv[1]
map_type = 'game'
game_mode = 1 # Creative
out_filename = sys.argv[2]
dtm_filename = sys.argv[3]
lcm_filename = sys.argv[4]
tf = sys.argv[5]

# remove existing map (else it just modifies)
rmtree(worlddir, True)

with open(tf, "a") as myfile:
    myfile.write("appended text\n")
    myfile.close()

# R-values from the texture TIFF are converted to blocks of the given
# blockID, blockData, depth.
block_id_lookup = {
    5 : (m.Sand.ID, m.Sand.blockData, 1), # Coastal
    9 : (3, 2, 0), # Bog
    4 : (m.WaterActive.ID, m.WaterActive.blockData, 1), # Water
    7 : (m.Stone.ID, m.Stone.blockData, 2), # Sea cliffs
    3 : (3, 1, 1), # Salt flats/marsh
    6 : (13, 0, 1), # vegitated shingle
    8 : (8, 0, 1), # non woodland river
    1 : (m.Dirt.ID, 2, 2), # non woodland bare area
    10 : (3, 2, 0), # Upland fens and swamp
    2 : (4, 0, 1), # littoral rock
    11 : (48, 0, 1), # Marsh fens and swamp
    12 : (m.Grass.ID, m.Grass.blockData, 2), # Calcareous grassland
    13 : (m.Grass.ID, m.Grass.blockData, 2), # Meadows and improved grassland
    14 : (m.Grass.ID, m.Grass.blockData, 2), # Heather grassland
    15 : (m.Grass.ID, m.Grass.blockData, 2), # Upland calcareous grassland
    16 : (m.Grass.ID, m.Grass.blockData, 2), # Non woodland-Grassland
    17 : (m.Dirt.ID, m.Dirt.blockData, 1), # upland heathland
    18 : (m.Dirt.ID, m.Dirt.blockData, 1), # Heather/moorland
    19 : (m.Grass.ID, m.Grass.blockData, 2), # broadleaf decidious woodland
    20 : (m.Grass.ID, m.Grass.blockData, 2), # Coniferous woodland
    21 : (m.Grass.ID, m.Grass.blockData, 2), # mixed woodland
    22 : (m.Grass.ID, m.Grass.blockData, 2), # lowdensity woodland/shrubs/coppice
    23 : (m.Cobblestone.ID, m.Cobblestone.blockData, 3), # inland limestone rock 
    24 : (m.Farmland.ID, 7, 0), # arable/agricultral land
    25 : (1, 6, 2), # Urban 
    251 : (1, 2, 2), # Suburban
    26 : (1, 2, 2), # windfarm
    27 : (56, 0, 2), # Quarry
    29 : (m.Farmland.ID, 7, 0), # beetroot
    30 : (m.Farmland.ID, 7, 0), # field bean
    31 : (m.Farmland.ID, 7, 0), # maize
    32 : (m.Farmland.ID, 7, 0), # oil seed rape
    33 : (m.Farmland.ID, 7, 0), # other
    34 : (m.Farmland.ID, 7, 0), # potatoes
    35 : (m.Farmland.ID, 7, 0), # spring barley
    36 : (m.Farmland.ID, 7, 0), # spring wheat
    37 : (m.Farmland.ID, 7, 0), # winter barley
    38 : (m.Farmland.ID, 7, 0), # winter wheat
    999 : (m.NoteBlock.ID, m.NoteBlock.blockData, 1), # unknown
}

#block_id_lookup = {
#    0 : (m.Grass.ID, None, 2),
#    10 : (m.Dirt.ID, 1, 1), # blockData 1 == grass can't spread
#    20 : (m.Grass.ID, None, 2),
#    30 : (m.Cobblestone.ID, None, 1),
#    40 : (m.StoneBricks.ID, None, 3),
#    200 : (m.Water.ID, 0, 2), # blockData 0 == normal state of water
#    210 : (m.WaterActive.ID, 0, 1),
#    220 : (m.Water.ID, 0, 1),
#}

plant_chance = {
    m.Watermelon.ID : 0.00001,
    m.Pumpkin.ID : 0.00001,
    m.SugarCane.ID : 0.01,
    "tree" : 0.001,
    m.TallGrass.ID : 0.003,
    "flower" : 0.0035,
}

def random_material():
    """Materials to be hidden underground to help survival play."""

    stone_chance = 0.90
    very_common = [m.Sand, m.Cobblestone, m.CoalOre, m.IronOre]
    common = [m.Clay, m.Obsidian, m.Gravel, m.MossStone, m.Dirt]
    uncommon = [m.RedstoneOre, m.LapisLazuliOre, m.GoldOre, 129]
    rare = [ m.Glowstone, m.DiamondOre, m.BlockofIron, m.TNT,
             m.BlockofGold, m.LapisLazuliBlock]
    very_rare = [ m.BlockofDiamond ]

    x = random.random()
    choice = None
    l = None
    if x < stone_chance:
        choice = m.Stone
    elif x < 0.96:
        l = very_common
    elif x < 0.985:
        l = common
    elif x < 0.998:
        l = uncommon
    elif x < 0.9995:
        l = rare
    else:
        l = very_rare
    if l is not None:
        choice = random.choice(l)
    if not isinstance(choice, int):
        choice = choice.ID
    return choice

with open(tf, "a") as myfile:
  myfile.write("Loading csvs for %s\n" % out_filename)
  myfile.close()
data = dict(elevation=[], features=[])

if not os.path.exists(dtm_filename):
    with open(tf, "a") as myfile:
      myfile.write("Could not load csv file %s!\n" % dtm_filename)
      myfile.close()
    sys.exit()

data['elevation'] = numpy.genfromtxt(dtm_filename, delimiter=',').astype(int)
    

if not os.path.exists(lcm_filename):
    with open(tf, "a") as myfile:
      myfile.write("Could not load csv file %s!\n" % lcm_filename)
      myfile.close()
    sys.exit()

data['features'] = numpy.genfromtxt(lcm_filename, delimiter=',').astype(int)

elevation= data['elevation']
material = data['features']

with open(tf, "a") as myfile:
  myfile.write("CSV is %s high, %s wide\n" % (len(elevation), len(elevation[0])))
  myfile.close()

# print "Scale factor: %s" % scale_factor

def setspawnandsave(world, point, tf):
    """Sets the spawn point and player point in the world and saves the world.

    Taken from TopoMC and tweaked to set biome.
    """
    with open(tf, "a") as myfile:
      myfile.write("Saving chunks\n")
      myfile.close()
      
    world.GameType = game_mode
    spawn = point
    spawn[1] += 2
    world.setPlayerPosition(tuple(point))
    world.setPlayerSpawnPosition(tuple(spawn))

    # In game mode, set the biome to Plains (1) so passive
    #  mobs will spawn.
    # In map mode, set the biome to Ocean (0) so they won't.
    if map_type == 'game':
        biome = 1
    else:
        biome = 0
    numchunks = 0
    biomes = TAG_Byte_Array([biome] * 256, "Biomes")
    for i, cPos in enumerate(world.allChunks, 1):
        ch = world.getChunk(*cPos)
        if ch.root_tag:
            ch.root_tag['Level'].add(biomes)
        numchunks += 1

    world.saveInPlace()
    with open(tf, "a") as myfile:
      myfile.write("Saved %d chunks.\n" % numchunks)
      myfile.close()

with open(tf, "a") as myfile:
  myfile.write("Creating world %s\n" % worlddir)
  myfile.close()

world = mclevel.MCInfdevOldLevel(worlddir, create=True)
from pymclevel.nbt import TAG_Int, TAG_String, TAG_Byte_Array
# Set Data tags #
tags = [TAG_Int(0, "MapFeatures"),
        TAG_String("flat", "generatorName"),
        TAG_String("0", "generatorOptions"),
        nbt.TAG_Long(name = 'DayTime', value = 4000)]
for tag in tags:
    world.root_tag['Data'].add(tag)

# Set Game rules #
rule = nbt.TAG_Compound(name = 'GameRules',
                        value = [TAG_String("false", "doDaylightCycle"),
                                 TAG_String("false", "doMobSpawning")])
world.root_tag['Data'].add(rule)

# The code tracks the peak [x,y,z]
# this is a placeholder
peak = [10, 255, 10]

x_extent = len(elevation)
x_min = 0
x_max = len(elevation)

z_min = 0
z_extent = len(elevation[0])
z_max = z_extent

#I think this leaves space for the glass walls?
extra_space = 1

# Sent minimum depth of earth
y_min = 10

bedrock_bottom_left = [-extra_space, 0,-extra_space]
bedrock_upper_right = [x_extent + extra_space + 1, y_min-1, z_extent + extra_space + 1]

glass_bottom_left = list(bedrock_bottom_left)
#glass_bottom_left[1] += 1
glass_upper_right = [x_extent + extra_space+1, 255, z_extent + extra_space+1]

air_bottom_left = (0,y_min,0)
air_upper_right = [x_extent, 255, z_extent]

# Glass walls
wall_material = m.Glass
with open(tf, "a") as myfile:
  myfile.write("Putting up walls: %r %r\n" % (glass_bottom_left, glass_upper_right))
  myfile.close()
  
tilebox = box.BoundingBox(glass_bottom_left, glass_upper_right)

with open(tf, "a") as myfile:
  myfile.write("Creating chunks.\n")
  myfile.close()
chunks = world.createChunksInBox(tilebox)
world.fillBlocks(tilebox, wall_material)

# Air in the middle.
bottom_left = (0, 1, 0)
upper_right = (len(elevation), 255, len(elevation[0]))
with open(tf, "a") as myfile:
  myfile.write("Carving out air layer. %r %r\n" % (bottom_left, upper_right))
  myfile.close()
tilebox = box.BoundingBox(bottom_left, upper_right)
world.fillBlocks(tilebox, m.Air, [wall_material])

with open(tf, "a") as myfile:
  myfile.write("Populating chunks.\n")
  myfile.close()
  
for x, row in enumerate(elevation):
  
    with open(tf, "a") as myfile:
      myfile.write("x = %r out of %r\n" % (x, x_extent))
      myfile.close()

    for z, y in enumerate(row):
        my_id = material[x][z]

        block_id, block_data, depth = block_id_lookup[my_id]
        actual_y = y + y_min
        if actual_y > peak[1] or (peak[1] == 255 and y != 0):
            peak = [x + 1, actual_y + 5, z]

        # Don't fill up the whole map from bedrock, just draw a shell.
        # this means there is a big cavern under everything... i think
        start_at = max(1, actual_y - depth - 10)

        # If we were going to optimize this code, this is where the
        # optimization would go. Lay down the stone in big slabs and
        # then sprinkle goodies into it.
        stop_at = actual_y-depth
        for elev in range(start_at, stop_at):
            if map_type == 'map' or elev == stop_at - 1:
                block = m.Stone.ID
            else:
                block = random_material()
            world.setBlockAt(x,elev,z, block)

        # now place the materials
        start_at = actual_y - depth
        stop_at = actual_y + 1
        
#        if random.random() < 0.25:
#            Chicken = Entity.Create('Chicken')
#            Entity.setpos(Chicken, (x, actual_y + 3, z))
#            world.addEntity(Chicken)
            
        # Add in if statements as you like for various special cases for placing materials
        if block_id == m.WaterActive.ID:
            # Carve a little channel for active water so it doesn't overflow.
            start_at -= 1
#            stop_at -= 1
            
            if random.random() < 0.2:
                Squid = Entity.Create('Squid')
                Entity.setpos(Squid, (x, actual_y - 1, z))
                world.addEntity(Squid)
        
        for elev in range(start_at, stop_at):
            world.setBlockAt(x, elev, z, block_id)
            if block_data:
                world.setBlockDataAt(x, elev, z, block_data)

        if my_id == 10: # Farm
            world.setBlockAt(x, elev + 1, z , 31)
            world.setBlockDataAt(x, elev + 1, z, 2)
        
        if my_id == 11: # Farm
            world.setBlockAt(x, elev + 1, z , 83)
            world.setBlockDataAt(x, elev + 1, z, 2)
        
        #if my_id == 13: # Improved grassland
        #    world.setBlockAt(x, elev + 1, z , 31)
        #    world.setBlockDataAt(x, elev + 1, z, 1)
        
        if my_id == 14: # Farm
            world.setBlockAt(x, elev + 1, z , 38)
            world.setBlockDataAt(x, elev + 1, z, 7)
        
        if my_id == 17: # Farm
            world.setBlockAt(x, elev + 1, z , 38)
            world.setBlockDataAt(x, elev + 1, z, 7)
        
        if my_id == 18: # Farm
            world.setBlockAt(x, elev + 1, z , 38)
            world.setBlockDataAt(x, elev + 1, z, 2)
        
        if my_id == 19: # SAPLING
            choice2 = random.random()
            if choice2 < 0.25:
                tree_pick = random.choice([0, 2, 3, 5])
                world.setBlockAt(x, elev + 1, z , m.Sapling.ID)
                world.setBlockDataAt(x, elev + 1, z, tree_pick)
            if choice2 > 0.2499999:
                world.setBlockAt(x, elev + 1, z , 31)
                world.setBlockDataAt(x, elev + 1, z, 1)
            if random.random() < 0.05: # add birds
                Parrot = Entity.Create('Parrot')
                Entity.setpos(Parrot, (x, actual_y + 3, z))
                Parrot['Variant'] = nbt.TAG_Int(random.choice([0,1,2,3]))
                world.addEntity(Parrot)
        
        if my_id == 20: # SAPLING
            choice2 = random.random()
            if choice2 < 0.25:
                world.setBlockAt(x, elev + 1, z , m.Sapling.ID)
                world.setBlockDataAt(x, elev + 1, z, 1)
            if random.random() < 0.05: # add birds
                Parrot = Entity.Create('Parrot')
                Entity.setpos(Parrot, (x, actual_y + 3, z))
                Parrot['Variant'] = nbt.TAG_Int(random.choice([0,1,2,3]))
                world.addEntity(Parrot)
        
        if my_id == 21: # SAPLING
            choice2 = random.random()
            if choice2 < 0.25:
                tree_pick = random.choice([0, 1, 2, 3, 4, 5])
                world.setBlockAt(x, elev + 1, z , m.Sapling.ID)
                world.setBlockDataAt(x, elev + 1, z, tree_pick)
            if random.random() < 0.05: # add birds
                Parrot = Entity.Create('Parrot')
                Entity.setpos(Parrot, (x, actual_y + 3, z))
                Parrot['Variant'] = nbt.TAG_Int(random.choice([0,1,2,3]))
                world.addEntity(Parrot)
        
        if my_id == 22: # SAPLING
            choice2 = random.random()
            if choice2 < 0.25:
                tree_pick = random.choice([0, 1, 2, 3, 4, 5])
                world.setBlockAt(x, elev + 1, z , m.Sapling.ID)
                world.setBlockDataAt(x, elev + 1, z, tree_pick)
            if random.random() < 0.05: # add birds
                Parrot = Entity.Create('Parrot')
                Entity.setpos(Parrot, (x, actual_y + 3, z))
                Parrot['Variant'] = nbt.TAG_Int(random.choice([0,1,2,3]))
                world.addEntity(Parrot)
                        
        if my_id == 24: # Farm
            world.setBlockAt(x, elev + 1, z , m.Crops.ID)
            world.setBlockDataAt(x, elev + 1, z, 6)
                    
        if my_id == 29: # Farm
            world.setBlockAt(x, elev + 1, z , 141)
            world.setBlockDataAt(x, elev + 1, z, 7)
        
        if my_id == 30: # Farm
            world.setBlockAt(x, elev + 1, z , 104)
            world.setBlockDataAt(x, elev + 1, z, 7)
        
        if my_id == 31: # Farm
            world.setBlockAt(x, elev + 1, z , m.Crops.ID)
            world.setBlockDataAt(x, elev + 1, z, 6)
        
        if my_id == 32: # Farm
            world.setBlockAt(x, elev + 1, z , 37)
            world.setBlockDataAt(x, elev + 1, z, 0)
        
        if my_id == 33: # Farm
            world.setBlockAt(x, elev + 1, z , 38)
            world.setBlockDataAt(x, elev + 1, z, 8)
        
        if my_id == 34: # Farm
            world.setBlockAt(x, elev + 1, z , 142)
            world.setBlockDataAt(x, elev + 1, z, 7)
        
        if my_id == 35: # Farm - spring barley
            world.setBlockAt(x, elev + 1, z , 175)
            world.setBlockDataAt(x, elev + 1, z, 2)
        
        if my_id == 36: # Farm - spring wheat
            world.setBlockAt(x, elev + 1, z , m.Crops.ID)
            world.setBlockDataAt(x, elev + 1, z, 2)
        
        if my_id == 37: # Farm - winter barley
            world.setBlockAt(x, elev + 1, z , 175)
            world.setBlockDataAt(x, elev + 1, z, 6)
        
        if my_id == 38: # Farm - winter wheat
            world.setBlockAt(x, elev + 1, z , m.Crops.ID)
            world.setBlockDataAt(x, elev + 1, z, 6)
        
        if my_id == 25: # Urban
            
            # set height width and depth randomly
            pH = random.random()
            if pH < 0.2:
                H = 10
            elif pH < 0.6:
                H = 8
            else:
                H = 6
                
            pW = random.random()
            if pW < 0.2:
                W = 4
            elif pW < 0.6:
                W = 3
            else:
                W = 2
                
            pD = random.random()
            if pD < 0.2:
                D = 4
            elif pD < 0.6:
                D = 3
            else:
                D = 2                    
                    
            if numpy.all(material[x-W:x+W, z-D:z+D] == 25): # Block of urban
                       
                MatPres = [] # empty array to get materials present
                
                for nY in range(actual_y + 1, actual_y + H + 2): # Loop through and see what is there
                    for nX in range(x - W - 2, x + W + 2): # extend x and y to allow 'streets'
                        for nZ in range(z - D - 1, z + D + 1):
                             MatPres.append(world.blockAt(nX,nY,nZ))
                             
                if all(item == 0 for item in MatPres): # If we have space to build the house
                    
                    wallMat = random.choice([(125,2), (98,0), (45,0)])
                    
                    for nY in range(actual_y - 1, actual_y + H + 1): # Loop through and build the house
                        
                        # set block type for level
                        if nY == max(range(actual_y + 1, actual_y + H + 1)): # Roof
                            blockType = random.choice([(44,0), (44,1), (44,5)])
                        elif nY - actual_y  == 2 or nY - actual_y == 4 or nY - actual_y == 6: # Windows level
                            blockType = (m.Glass.ID, 0)
                        else: # Wall
                            blockType = wallMat
                            
                        for nX in range(x - W, x + W):
                            
                            # make pillars and place block
                            for nZ in range(z - D, z + D):
                                
                                bT = blockType # save to reset
                                
                                # Make pillars
                                xEdge = nX == min(range(x - W, x + W)) or nX == max(range(x - W, x + W))
                                zEdge = nZ == min(range(z - D, z + D)) or nZ == max(range(z - D, z + D))
                                if xEdge and zEdge:
                                        if nY != max(range(actual_y + 1, actual_y + H + 1)):
                                            blockType = wallMat                       
                                
                                if nY - actual_y < 1:
                                    blockType = (1, 6)
                                
                                world.setBlockAt(nX, nY, nZ, blockType[0])
                                world.setBlockDataAt(nX, nY, nZ, blockType[1])
                                
                                blockType = bT
                else: # urban but we can't put a house
                    if random.random() < 0.01: # Add a cat
                        Cat = Entity.Create('Ocelot')
                        Entity.setpos(Cat, (x, actual_y + 2, z)) # Where to put it
                        Cat['CatType'] = nbt.TAG_Int(random.choice([1,2,3])) # What kind of cat
                        world.addEntity(Cat) # Add it
                    if random.random() < 0.1: # Add a person
                        Villager = Entity.Create('Villager')
                        Entity.setpos(Villager, (x, actual_y + 2, z)) # Where to put it
                        Villager['Profession'] = nbt.TAG_Int(random.choice([0,1,2,3,4,5])) # What kind of cat
                        world.addEntity(Villager) # Add it
                        
                        
        if my_id == 251: # Suburban
            
            # set height width and depth randomly
            pH = random.random()
            if pH < 0.2:
                H = 6
            elif pH < 0.6:
                H = 4
            else:
                H = 4
                
            pW = random.random()
            if pW < 0.2:
                W = 4
            elif pW < 0.6:
                W = 3
            else:
                W = 2
                
            pD = random.random()
            if pD < 0.2:
                D = 4
            elif pD < 0.6:
                D = 3
            else:
                D = 2                    
                    
            if numpy.all(material[x-W:x+W, z-D:z+D] == 251): # Block of urban
                       
                MatPres = [] # empty array to get materials present
                
                for nY in range(actual_y + 1, actual_y + H + 2): # Loop through and see what is there
                    for nX in range(x - W - 2, x + W + 2): # extend x and y to allow 'streets'
                        for nZ in range(z - D - 1, z + D + 1):
                             MatPres.append(world.blockAt(nX,nY,nZ))
                             
                if all(item == 0 for item in MatPres): # If we have space to build the house
                    
                    wallMat = random.choice([(43,2), (125,5), (125,3)])
                    
                    for nY in range(actual_y - 1, actual_y + H + 1): # Loop through and build the house
                        
                        # set block type for level
                        if nY == max(range(actual_y + 1, actual_y + H + 1)): # Roof
                            blockType = random.choice([(126,1), (126,3), (126,5)])
                        elif nY - actual_y  == 2 or nY - actual_y == 4 or nY - actual_y == 6: # Windows level
                            blockType = (m.Glass.ID, 0)
                        else: # Wall
                            blockType = wallMat
                            
                        for nX in range(x - W, x + W):
                            
                            # make pillars and place block
                            for nZ in range(z - D, z + D):
                                
                                bT = blockType # save to reset
                                
                                # Make pillars
                                xEdge = nX == min(range(x - W, x + W)) or nX == max(range(x - W, x + W))
                                zEdge = nZ == min(range(z - D, z + D)) or nZ == max(range(z - D, z + D))
                                if xEdge and zEdge:
                                        if nY != max(range(actual_y + 1, actual_y + H + 1)):
                                            blockType = wallMat                       
                                
                                if nY - actual_y < 1:
                                    blockType = (1, 6)
                                
                                world.setBlockAt(nX, nY, nZ, blockType[0])
                                world.setBlockDataAt(nX, nY, nZ, blockType[1])
                                
                                blockType = bT
                else: # urban but we can't put a house
                    if random.random() < 0.01: # Add a cat
                        Cat = Entity.Create('Ocelot')
                        Entity.setpos(Cat, (x, actual_y + 2, z)) # Where to put it
                        Cat['CatType'] = nbt.TAG_Int(random.choice([1,2,3])) # What kind of cat
                        world.addEntity(Cat) # Add it
                    if random.random() < 0.02: # Add a person
                        Villager = Entity.Create('Villager')
                        Entity.setpos(Villager, (x, actual_y + 2, z)) # Where to put it
                        Villager['Profession'] = nbt.TAG_Int(random.choice([0,1,2,3,4,5])) # What kind of cat
                        world.addEntity(Villager) # Add it                
        
        if my_id == 12: # Grassland
            choice = random.random()
            if choice < 0.5:
                if choice < 0.25:
                    world.setBlockAt(x, elev + 1, z , 38)
                    world.setBlockDataAt(x, elev + 1, z, 0)
                else:
                    world.setBlockAt(x, elev + 1, z , 37)
                    world.setBlockDataAt(x, elev + 1, z, 0)
        else: pass
      
#        world.setBlockAt(x, elev + 1, z , m.Crops.ID)
#        world.setBlockDataAt(x, elev + 1, z, 7)

        # In game mode, sprinkle some semi-realistic outdoor features
        # onto the grass. 
        #WE PROBABLY WANT TO CONTROL THIS OURSELVES
#        if map_type == "game" and block_id == m.Grass.ID:
#            for plant, probability in plant_chance.items():
#                choice = random.random()
#                if choice < probability:
#                    if plant == 'tree':
#                        # Plant a TopoMC tree here.
#                        tree_type = random.choice([2,4,5,5])
#                        # print "Planting a tree at (%s,%s,%s)" % (x, elev+1, z)
#                        (blocks, block_data) = treeObjs[tree_type]((x,elev+1,z))
#                        [world.setBlockAt(tx, ty, tz, block.ID) for (tx, ty, tz, block) in blocks if block != m.Air and tx >= x_min and tz >= z_min and tx <= x_max and tz <= z_max]
#                        [world.setBlockDataAt(tx, ty, tz, bdata) for (tx, ty, tz, bdata) in block_data if bdata != 0 and tx >= x_min and tz >= z_min and tx <= x_max and tz <= z_max]
#                    elif plant == 'flower':
#                        # Plant a flower, nothing too fancy.
#                        id, data = random.choice(
#                            [(37,None), (38,None), (38,3), (38,8)])
#                        world.setBlockAt(x, elev+1,z, id)
#                        if data:
#                            world.setBlockDataAt(x, elev+1,z, data)
#                    elif plant == m.SugarCane.ID:
#                        # Must be next to water
#                        for water_x in (x-1, x+1):
#                            for water_z in (z-1, z+1):
#                                data = world.blockAt(water_x, y, water_z)
#                                if data == m.Water.ID:
#                                    # Yay, we found water.
#                                    world.setBlockAt(x, elev+1, z, plant)
#                                    # print "Yay, water at %s, %s, %s" % (x, elev+1,z)
#                    else:
#                        world.setBlockAt(x, elev+1,z, plant)
#                    break

setspawnandsave(world, peak, tf)