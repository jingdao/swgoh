#!/usr/bin/python

import os
import re
import sys
download_data = False
f = open('url.txt','r')
l = f.read()
m = re.findall('href="(.*?)">',l)
attr = ['Health','Speed','Health Steal','Physical Critical Rating','Special Critical Rating','Potency','Tenacity']
heroes={}
for mm in m:
	t = mm.split('/')
	name = t[-1] if t[-1] else t[-2]
	if download_data:
		os.system('wget -nc -O data/'+name+".data http://swgoh.gg"+mm+"80/")
	g = open('data/'+name+'.data','r')
	data={}
	data['numActiveAbility']=0
	abilities=[]
	while True:
		s = g.readline()
		if not s:
			break
		for a in attr:
			if a in s:
				m = re.search('([\d%]*)</div>'+a+'<',s)
				if m:
					data[a]=m.group(1)
		if 'src' in s:
			m = re.search('ability(.*?)title="(.*?)"',s)
			if m:
				abilities.append(m.group(2))
				if not 'passive' in m.group(1):
					data['numActiveAbility'] += 1
		if 'strong' in s:
			m = re.search('(\d*) - (\d*)',s)
			if m:
				abilities.append(m.group(1))
				abilities.append(m.group(2))
		if 'cooldown' in s:
			m = re.search('(\d) turn cooldown',s)
			if m:
				abilities.append(m.group(1))
	data['abilities'] = abilities
	heroes[name]=data
	g.close()
f.close()

def proper_name(s):
	s = s.replace('-','_').upper()
	s = s.replace("FIRST_ORDER","FO")
	s = s.replace("HOTH_REBEL","HR")
	s = s.replace("JEDI_KNIGHT","JK")
	s = s.replace("NIGHTSISTER","NS")
	s = s.replace("STORMTROOPER","STORMTR")
	s = s.replace("RESISTANCE","RES")
	return s

outheader=open('hero.h','w')
outfile=open('hero.c','w')
typedef="""
typedef struct {
	char* name;
	float hp;
	int speed;
	float hp_steal;
	float phy_crit;
	float sp_crit;
	float potency;
	float tenacity;
	int numActiveAbility;
	char* ability[5];
	float min_damage[5];
	float max_damage[5];
	int cooldown[5];
} Hero;
"""
outheader.write(typedef)
outheader.write('extern Hero* ROSTER['+str(len(heroes))+'];\n')
outfile.write('#include "hero.h"\n')
for h in sorted(heroes.keys()):
	pn = proper_name(h)
	outheader.write('extern Hero '+pn+';\n')
	s = 'Hero '+pn+' = {"'+pn+'",';
	for a in attr:
		val = heroes[h][a]
		if val[-1] == '%':
			s += str(0.01*int(val[:-1]))+','
		else:
			s += val + ','
	s += str(heroes[h]['numActiveAbility'])+','
	ability=[""]*5
	min_damage=["0"]*5
	max_damage=["0"]*5
	cooldown=["0"]*5
	index=-1
	mode=0
	for i in range(len(heroes[h]['abilities'])):
		a = heroes[h]['abilities'][i]
		if a.isdigit():
			if mode==0:
				cooldown[index]=a
				mode=1
			elif mode == 1:
				min_damage[index]=a
				mode=2
			elif mode == 2:
				max_damage[index]=a
				mode=0
		else:
			index += 1
			ability[index] = a.replace("&#39;","")
			mode = 1 if index==0 else 0
	s += '{'
	for i in range(4):
		s += '"'+ ability[i] + '",'
	s += '"'+ability[4]+'"},{'
	for i in range(4):
		s += min_damage[i] + ','
	s += min_damage[4]+'},{'
	for i in range(4):
		s += max_damage[i] + ','
	s += max_damage[4]+'},{'
	for i in range(4):
		s += cooldown[i] + ','
	s += cooldown[4]+'}};\n'
	outfile.write(s)
s="Hero* ROSTER["+str(len(heroes))+"] = {"
for h in sorted(heroes.keys()):
	pn = proper_name(h)
	s += '&' + pn + ','
outfile.write(s[:-1]+'};\n')
outheader.close()
outfile.close()
