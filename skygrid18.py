# SkyGrid Filter by SethBling
# edit by dodieboy
# Feel free to modify and reuse, but credit to SethBling would be nice.

from pymclevel import MCSchematic
from pymclevel import TileEntity
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_String
import random
from random import randint

displayName = "Sky Grid 1.8"
inputs = (
	("Grid Length", (4, 1, 100)),
	("World Type", ("Overworld",
					"Nether",
					)),
)

def perform(level, box, options):
	gridlength = options["Grid Length"]
	worldtype = options["World Type"]

	total = 0
	cump = {}

	if worldtype == "Overworld":
		p = normalp()
	elif worldtype == "Nether":
		p = netherp()

	# generate the cumulative distribution
	for key, value in p.iteritems():
		cump[key] = (total, total + value)
		total += value
			
	for x in xrange(box.minx, box.maxx, gridlength):
		for y in xrange(box.miny, box.maxy, gridlength):
			for z in xrange(box.minz, box.maxz, gridlength):
				blockid = pickblock(cump, total)

				if(blockid == 6 or blockid == 31 or blockid == 32 or blockid == 37 or
				   blockid == 38 or blockid == 39 or blockid == 40 or blockid == 83 or
				   blockid == 171):
					level.setBlockAt(x, y, z, 3) #dirt
					if(y < box.maxy):
						level.setBlockAt(x, y+1, z, blockid)
					if(blockid == 83): #reeds
						level.setBlockAt(x+1, y, z, 9) #still water
				
				elif(blockid == 81): #cactus
					level.setBlockAt(x, y, z, 12) #sand
					if(y < box.maxy):
						level.setBlockAt(x, y+1, z, blockid)
					if(y > box.miny):
						level.setBlockAt(x, y-1, z, 106) # vines
				
				elif(blockid == 111): #lillypad
					level.setBlockAt(x, y, z, 9) # still water
					level.setBlockAt(x, y+1, z, blockid)
				
				elif blockid == 17 or blockid == 18: #leaves and logs
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 3))
	
				elif blockid == 159 or blockid == 171 or blockid == 95: #stained clay and glass and carpet
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 15))
		
				elif(blockid == 117): #brewing stand
					level.setBlockAt(x, y, z, 87) #netherack
					level.setBlockAt(x, y+1, z, blockid)
				
				elif blockid == 161 or blockid == 162: #new leaves and logs
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 1))

				elif blockid == 1: #stone
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 6))
				
				elif blockid == 3: #dirt
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 2))
				
				elif blockid == 12: #sand
					level.setBlockAt(x, y, z, blockid)
					level.setBlockDataAt(x, y, z, randint(0, 1))
				
				elif blockid == 141 or blockid == 142 or blockid == 59: #carrots and potatoes
					level.setBlockAt(x, y, z, 60)
					level.setBlockAt(x, y+1, z, blockid)
				
				elif(blockid == 115): # netherwart
					level.setBlockAt(x, y, z, 88)
					if(y < box.maxy):
						level.setBlockAt(x, y+1, z, blockid)
				else:
					level.setBlockAt(x, y, z, blockid)
				
				if(blockid == 54):
					fillChestAt(level, x, y, z)

				if(blockid == 52):
					setSpawnerAt(level, worldtype, x, y, z)

	if worldtype == "Overworld":
		#generate end portal
		dx = box.maxx - box.minx
		dz = box.maxz - box.minz

		middlex = box.minx + int(dx / 2 / gridlength) * gridlength
		middlez = box.minz + int(dz / 2 / gridlength) * gridlength
		
		y = box.miny + gridlength

		if y <= box.maxy and middlex+4 <= box.maxx and middlez+4 <= box.maxz:
			# set portal blocks
			level.setBlockAt(middlex+1, y, middlez, 120)
			level.setBlockAt(middlex+2, y, middlez, 120)
			level.setBlockAt(middlex+3, y, middlez, 120)

			level.setBlockAt(middlex, y, middlez+1, 120)
			level.setBlockAt(middlex, y, middlez+2, 120)
			level.setBlockAt(middlex, y, middlez+3, 120)

			level.setBlockAt(middlex+1, y, middlez+4, 120)
			level.setBlockAt(middlex+2, y, middlez+4, 120)
			level.setBlockAt(middlex+3, y, middlez+4, 120)

			level.setBlockAt(middlex+4, y, middlez+1, 120)
			level.setBlockAt(middlex+4, y, middlez+2, 120)
			level.setBlockAt(middlex+4, y, middlez+3, 120)

			# set damage values
			level.setBlockDataAt(middlex+1, y, middlez, 0)
			level.setBlockDataAt(middlex+2, y, middlez, 0)
			level.setBlockDataAt(middlex+3, y, middlez, 0)

			level.setBlockDataAt(middlex, y, middlez+1, 3)
			level.setBlockDataAt(middlex, y, middlez+2, 3)
			level.setBlockDataAt(middlex, y, middlez+3, 3)

			level.setBlockDataAt(middlex+1, y, middlez+4, 2)
			level.setBlockDataAt(middlex+2, y, middlez+4, 2)
			level.setBlockDataAt(middlex+3, y, middlez+4, 2)

			level.setBlockDataAt(middlex+4, y, middlez+1, 1)
			level.setBlockDataAt(middlex+4, y, middlez+2, 1)
			level.setBlockDataAt(middlex+4, y, middlez+3, 1)
	

	level.markDirtyBox(box)

# returns an unnormalized probability distribution for blocks in the
# overworld
def normalp():
	p = {}
	p[1] = 150  #stone
	p[2] = 80   #grass
	p[3] = 25   #dirt
	p[9] = 5    #still water
	p[11] = 5   #still lava
	p[12] = 30  #sand
	p[13] = 10  #gravel
	p[14] = 10  #gold ore
	p[15] = 20  #iron ore
	p[16] = 50  #coal ore
	p[17] = 100  #log
	p[18] = 30  #leaves
	p[19] = 1   #sponge
	p[20] = 2   #glass
	p[21] = 6   #lapis ore
	p[24] = 10  #sandstone
	p[29] = 1   #sticky piston
	p[30] = 10  #web
	p[31] = 3   #shrub
	p[32] = 3   #shrub
	p[33] = 1   #piston
	p[35] = 30  #wool
	p[37] = 2   #yellow flower
	p[38] = 2   #red flower
	p[39] = 2   #brown mushroom
	p[40] = 2   #red mushroom
	p[46] = 2   #TNT
	p[47] = 4   #bookshelves
	p[48] = 5   #mossy cobblestone
	p[49] = 4   #obsidian
	p[52] = 1   #spawner
	p[54] = 1   #chest
	p[56] = 2   #diamond ore
	p[59] = 3	#wheat
	p[73] = 10  #redstone ore
	p[79] = 4   #ice
	p[80] = 6   #snow
	p[81] = 1   #cactus
	p[82] = 20  #clay
	p[83] = 15  #reeds
	p[86] = 5   #pumpkin
	p[95] = 2	#stained glass
	p[97] = 5   #stone monster egg
	p[98] = 30  #stone brick
	p[103] = 5  #melon
	p[110] = 15 #mycelium
	p[111] = 5  #lillypad
	p[129] = 8  #emerald ore
	p[141] = 3  #carrot
	p[142] = 3  #potato
	p[152] = 1	#redstone block
	p[158] = 1  #dropper
	p[159] = 12 #colour stained clay
	p[161] = 20 #new leaves
	p[162] = 50 #new log
	p[165] = 2  #slime block
	p[170] = 15 #hay block
	p[171] = 10 #carpet
	p[172] = 12 #stained clay
	p[174] = 4  #packet ice
	p[179] = 10 #red sandstone
	
	

	return p

# returns an unnormalized probability distribution for blocks in the
# nether
def netherp():
	p = {}
	p[11] = 60  #still lava
	p[13] = 35  #gravel
	p[52] = 1   #mob spawner
	p[54] = 1   #chest
	p[49] = 8   #obsidian
	p[87] = 340 #netherack
	p[88] = 100 #soulsand
	p[89] = 50  #glowstone
	p[91] = 35  #jack o'lantern
	p[101] = 25 #iron bar
	p[112] = 35 #nether brick
	p[113] = 10 #nether fence
	p[114] = 15 #nether stairs
	p[115] = 40 #netherwart
	p[117] = 5	#brewing stand	
	p[153] = 55 #quartz ore
	p[173] = 10 #coal block
	return p

# picks a random block from a cumulative distribution
def pickblock(cump, size):
	r = random.random() * size
	
	for key, value in cump.iteritems():
		low, high = value
		if r >= low and r < high:
			return key

# creates a randomized mob spawner tile entity at a specified location
def setSpawnerAt(level, worldtype, x, y, z):
	chunk = level.getChunk(x / 16, z / 16)

	if worldtype=="Overworld":
		spawns = overworldSpawns()
	elif worldtype=="Nether":
		spawns = netherSpawns()
		
	spawnindex = randint(0, len(spawns) - 1)

	spawner = TileEntity.Create("MobSpawner")
	TileEntity.setpos(spawner, (x, y, z))
	spawner["Delay"] = TAG_Short(120)
	spawner["EntityId"] = TAG_String(spawns[spawnindex])

	chunk.TileEntities.append(spawner)

def overworldSpawns():
	return ["Creeper",
			"Skeleton",
			"Spider",
			"CaveSpider",
			"Zombie",
			"Slime",
			"Pig",
			"Sheep",
			"Cow",
			"Chicken",
			"Squid",
			"Wolf",
			"Enderman",
			"Silverfish",
			"Villager",
			"Bat",
			"MushroomCow",
			"Ozelot",
			"Witch",
			"Guardian",
			"Rabbit",
			"Horse",
			]

def netherSpawns():
	return ["PigZombie",
			"Blaze",
			"LavaSlime",
			"Skeleton",
			"Ghast",
			]

# fills a chest with random goodies
def fillChestAt(level, x, y, z):
	chunk = level.getChunk(x / 16, z / 16)

	chest = TileEntity.Create("Chest")
	TileEntity.setpos(chest, (x, y, z))

	if(random.random() < 0.8):
		chest["Items"].append(createItemInRange(256, 294)) #various weapons/random

	if(random.random() < 0.8):
		chest["Items"].append(createItemInRange(298, 317)) #various armor

	if(random.random() < 0.9):
		chest["Items"].append(createItemInRange(318, 350)) #various food/tools

	if(random.random() < 0.9):
		chest["Items"].append(createItemInRange(351, 351)) #various food/tools
	
	if(random.random() < 0.3):
		chest["Items"].append(createItemWithRandomDamage(383, 50, 52)) # various spawn eggs

	if(random.random() < 0.9):
		chest["Items"].append(createItemWithRandomDamage(383, 54, 62)) #various spawn eggs
		
	if(random.random() < 0.2):
		chest["Items"].append(createItemWithRandomDamage(383, 65, 68)) #various spawn eggs

	if(random.random() < 0.4):
		chest["Items"].append(createItemWithRandomDamage(383, 90, 96)) #various spawn eggs

	if(random.random() < 0.2):
		chest["Items"].append(createItemWithRandomDamage(383, 98, 98)) #ocelot spawn egg

	if(random.random() < 0.1):
		chest["Items"].append(createItemWithRandomDamage(383, 120, 120)) #villager spawn egg
		
	if(random.random() < 0.4):
		chest["Items"].append(createItemWithRandomDamage(383, 101, 101)) #rabbit spawn egg
	
	if(random.random() < 0.1):
		chest["Items"].append(createItemWithRandomDamage(383, 100, 100)) #horse spawn egg
	
	if random.random() < 0.1:
		chest["Items"].append(createItemWithRandomDamage(397, 0, 4)) # masks

	if(random.random() < 0.9):
		itemid = randint(1, 5)
		count = randint(10, 64)
		slot = randint(0, 26)
		blocks = createItem(itemid, count, 0, slot)
		chest["Items"].append(blocks)

	sapling = createItemWithRandomDamage(6, 0, 5)
	sapling["Slot"] = TAG_Byte(randint(0, 26))
	chest["Items"].append(sapling)

	chunk.TileEntities.append(chest)

# creates a random item in an item id range    
def createItemInRange(minid, maxid, count=1):
	itemid = randint(minid, maxid)
	slot = randint(0, 26)

	return createItem(itemid, count, 0, slot)

# creates an item with a randomized damage value
def createItemWithRandomDamage(itemid, mindmg, maxdmg, count=1):
	dmg = randint(mindmg, maxdmg)
	slot = randint(0, 26)
	
	return createItem(itemid, count, dmg, slot)

# creates an item
def createItem(itemid, count=1, damage=0, slot=0):
	item = TAG_Compound()

	item["id"] = TAG_Short(itemid)
	item["Damage"] = TAG_Short(damage)
	item["Count"] = TAG_Byte(count)
	item["Slot"] = TAG_Byte(slot)

	return item
