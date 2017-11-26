f = open("map.txt")
game_map = [['-','-','-','-'],['-','-','-','-'],['-','-','-','-'],['-','-','-','-']]
i = 0
line = f.readline()
while line:
	# print line,
	
	game_map[i/4][i%4] = line
	i += 1
	line = f.readline()
f.close()
for i in range(4):
	for j in range(4):
		game_map[i][j] = game_map[i][j].strip()
print game_map
