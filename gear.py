#!/usr/bin/python

import sys
import re

gear_names=[]
rarity={}
f = open('farmable_gear.csv','r')
f.readline()
f.readline()
ind=0
for l in f:
	t = l.split(',')
	gear_names.append(t[1])
	name = t[1].lower()
	val = t[3]
	rarity[name]=(val,ind)
	ind += 1

proper_names=[]
for g in gear_names:
	r=re.match(r"(.*?)\(Mk (\d)\)(.*)",g)
	s="Mk "+r.group(2)+" "+r.group(1).strip()+r.group(3)
	proper_names.append(s.replace(' ','-').replace('/',''))

ingredients={}
f = open('craftable_gear.csv','r')
f.readline()
f.readline()
for l in f:
	t = l.split(',')
	name = t[1].lower()
	i = 6
	ingredients[name]={}
	req=[]
	num=[]
	while i<len(t)-2 and t[i]:
		num.append(int(t[i]))
		req.append(t[i+2].lower())
		i += 3
	ingredients[name]['req']=req
	ingredients[name]['num']=num

def blankCost():
	return {'C':{},'U':{},'R':{},'E':{}}

totalCost = {}

def getCost(i):
	if i in totalCost:
		return totalCost[i]
	d=blankCost()
	if not i in ingredients:
		d[rarity[i][0]] = {i:1}
	else:
		req=ingredients[i]['req']
		num=ingredients[i]['num']
		for j in range(len(req)):
			ct = getCost(req[j])
			for c in ct:
				for k in ct[c]:
					if k in d[c]:
						d[c][k] += ct[c][k] * num[j]
					else:
						d[c][k] = ct[c][k] * num[j]
	totalCost[i] = d
	return d

def getGearCount(cost):
	d={}
	for c in cost:
		d[c]=0
		for k in cost[c]:
			d[c] += cost[c][k]
	return d

for i in ingredients:
	if not i in totalCost:
		getCost(i)
for i in rarity:
	if not i in totalCost:
		getCost(i)

hero_names=[]
heroes={}
maxGearLevel=12
f = open('ultimatox.csv','r')
f.readline()
l=f.readline().split(',')
i=2
while i<len(l)-1 and l[i]:
	hero_names.append(l[i])
	heroes[l[i]] = []
	i+=2

for level in range(maxGearLevel):
	levelCost={}
	for h in hero_names:
		levelCost[h] = blankCost()
	for slot in range(6):
		l=f.readline().split(',')
		j=2
		for i in range(len(hero_names)):
			ct = totalCost[l[j].lower()]
			for c in ct:
				for k in ct[c]:
					if k in levelCost[hero_names[i]][c]:
						levelCost[hero_names[i]][c][k] += ct[c][k]
					else:
						levelCost[hero_names[i]][c][k] = ct[c][k]
			j+=2
	for h in hero_names:
		heroes[h].append(levelCost[h])

def printHeroGear(hr,targetLevel=9):
	s = ''
	aggregate = blankCost()
	gearColor = {'C':'GRAY','U':'GREEN','R':'BLUE','E':'PURPLE'}
	for level in range(min(targetLevel,maxGearLevel)):
		ct = heroes[hr][level]
		num = getGearCount(ct)
		s += 'LEVEL %d (%d,%d,%d,%d)\n' % (level+1,num['C'],num['U'],num['R'],num['E'])
		for c in ['C','U','R','E']:
			s += gearColor[c]+'\n'
			for k in ct[c]:
				s += '%-60s %d\n' % (k,ct[c][k])
				if k in aggregate[c]:
					aggregate[c][k] += ct[c][k]
				else:
					aggregate[c][k] = ct[c][k]
			s += '\n'
	num = getGearCount(aggregate)
	s += 'TOTAL (%d,%d,%d,%d)\n'% (num['C'],num['U'],num['R'],num['E'])
	for c in ['C','U','R','E']:
		s += gearColor[c]+'\n'
		for k in aggregate[c]:
			s += '%-60s %d\n' % (k,aggregate[c][k])
		s += '\n'
	return s

def getTex(hr,targetLevel=9):
	s = "\\documentclass[twoside,12pt]{article}\n"+ \
		"\\usepackage{graphicx}\n"+ \
		"\\newcommand{\\imsize}{0.1\\linewidth}\n"+ \
		"\\begin{document}\n" + \
		"\\title{"+hr.replace('"','')+"}\n" + \
		"\\maketitle\n"
	aggregate = blankCost()
	gearColor = {'C':'GRAY','U':'GREEN','R':'BLUE','E':'PURPLE'}
	for level in range(min(targetLevel,maxGearLevel)):
		ct = heroes[hr][level]
		num = getGearCount(ct)
		s += '\\section*{LEVEL %d (%d,%d,%d,%d)}\n' % (level+1,num['C'],num['U'],num['R'],num['E'])
		for c in ['C','U','R','E']:
			s += '\\subsection*{'+gearColor[c]+'}\n'
			for k in ct[c]:
				s += '\\includegraphics[width=\\imsize]{images/'+proper_names[rarity[k][1]]+'} '+str(ct[c][k])+'\n'
				if k in aggregate[c]:
					aggregate[c][k] += ct[c][k]
				else:
					aggregate[c][k] = ct[c][k]
		s += '\\newpage\n'
	num = getGearCount(aggregate)
	s += '\\section*{TOTAL (%d,%d,%d,%d)}\n' % (num['C'],num['U'],num['R'],num['E'])
	for c in ['C','U','R','E']:
		s += '\\subsection*{'+gearColor[c]+'}\n'
		for k in aggregate[c]:
			s += '\\includegraphics[width=\\imsize]{images/'+proper_names[rarity[k][1]]+'} '+str(aggregate[c][k])+'\n'
	s += '\\end{document}\n'
	return s


def getDemand(targetLevel=9):
	demand={}
	for h in heroes:
		aggregate = blankCost()
		for level in range(min(targetLevel,maxGearLevel)):
			ct = heroes[h][level]
			for c in aggregate:
				for k in ct[c]:
					if k in aggregate[c]:
						aggregate[c][k] += ct[c][k]
					else:
						aggregate[c][k] = ct[c][k]
		for c in aggregate:
			for k in aggregate[c]:
				if k in demand:
					demand[k]['freq'] += aggregate[c][k]
					demand[k]['usage'] += 1
				else:
					demand[k] = {'freq':aggregate[c][k],'usage':1}
	return demand

if __name__=="__main__":
	l = len(sys.argv)
	if l == 3:
		print printHeroGear(sys.argv[1],int(sys.argv[2]))
	elif l == 2:
		if sys.argv[1]=='-h':
			for h in hero_names:
				print h
		elif sys.argv[1]=='-g':
			for g in proper_names:
				print g
		elif sys.argv[1]=='-p':
			for h in hero_names:
				f=open('pdf/'+h.replace(' ','_').replace('"','').replace("'",'')+'.tex','w')
				f.write(getTex(h))
				f.close()
		else:
			hr = sys.argv[1]
			if not hr in heroes:
				for h in heroes:
					if hr in h:
						hr = h
						break
			print printHeroGear(hr)
	else:
		demand = getDemand()
		ls = []
		for d in demand:
			ls.append([d,demand[d]['freq'],demand[d]['usage']])
		print 'FREQUENCY'
		for d in sorted(ls,key=lambda l:l[1],reverse=True):
			print "%-60s %1s %4d %4d" % (d[0],rarity[d[0]][0],d[1],d[2])
		print '\nUSAGE'
		for d in sorted(ls,key=lambda l:l[2],reverse=True):
			print "%-60s %1s %4d %4d" % (d[0],rarity[d[0]][0],d[1],d[2])

					


