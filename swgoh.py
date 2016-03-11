#!/usr/bin/python
header = """
   Name
   Health
   Speed
   B-Dam
   Phy CR
   Spec CR
   Armor
   Armor Pen
   Resist
   Resist Pen
   Potency
   Tenacity
   HP Steal
"""
data="""   
   Savage Opress 22843 123 5250 6111 477 50 252 32 167 5 108% 39% 30%
   Boba Fett 15471 101 4615 2750 624 10 256 44 145 0 116% 65% 0%
   Jedi Consular 14233 119 4538 5220 418 90 182 32 155 32 35% 43% 5%
   Barriss Offee 25439 122 2634 444 90 253 41 167 5 110% 54% 5%
   Aayla Secura 24084 119 4465 8162 693 60 252 25 81 15 95% 61% 10%
   Count Dooku 14651 161 4743 5107 644 70 196 70 142 10 342% 51% 0%
   Old Daka 19245 136 3768 309 65 198 49 225 30 187% 49% 0%
   Grand Moff Tarkin 13866 102 4353 2772 374 195 243 17 275 32 79% 42% 10%
   Mace Windu 19684 123 3606 7237 260 95 255 15 360 20 137% 71% 0%
   Obi-Wan Kenobi (Old Ben) 27990 112 4505 353 10 477 20 242 5 98% 59% 15%
   Plo Koon 19313 126 4195 2194 250 95 342 16 308 25 100% 63% 0%
   General Veers 15067 125 4719 2604 418 15 211 30 209 44 142% 48% 5%
   Luminara Unduli 17213 124 5053 7477 709 75 239 28 159 0 142% 43% 5%
   Darth Maul 11393 94 6393 6209 1005 0 195 99 76 0 20% 28% 20%
   Darth Sidious 12815 161 5259 4382 858 20 234 50 146 15 54% 62% 15%
   Poggle the Lesser 19039 144 3840 329 175 187 20 157 54 193% 50% 0%
   Asajj Ventress 16093 106 5399 3929 705 45 270 27 116 27 60% 42% 50%
   Clone Wars Chewbacca 27054 106 3114 487 70 267 101 108 0 122% 50% 10%
   Jawa 14196 130 4705 3856 304 105 245 46 176 30 155% 43% 5%
   Talia 17548 109 3451 6351 316 125 215 45 232 5 190% 50% 5%
   IG-100 MagnaGuard 27871 99 4202 2933 360 10 284 20 261 10 147% 54% 15%
   Royal Guard 32956 110 3949 294 10 304 34 238 0 158% 77% 10%
   Clone Sergeant - Phase 1 15919 101 5233 3171 768 60 230 42 144 5 20% 42% 10%
   Snowtrooper 22811 112 5010 4117 588 60 223 54 182 5 131% 43% 10%
   URoRRuR'R'R 14574 147 4713 381 110 180 49 185 20 79% 50% 0%
   Eeth Koth 15995 132 3654 6763 310 120 183 47 268 17 200% 41% 0%
   Ewok Scout 14775 127 5168 7775 817 80 233 26 99 0 80% 47% 10%
   Dathcha 14206 131 5309 3134 536 50 244 60 154 25 170% 33% 20%
   Hoth Rebel Soldier 27263 98 4196 394 80 243 71 134 5 172% 44% 5%
   CT-5555 Fives 31535 119 3351 5251 382 10 453 34 83 0 92% 59% 15%
   IG-88 12566 121 6115 3807 846 70 202 27 129 10 72% 45% 15%
   IG-86 Sentinel Droid 15515 125 6496 7868 804 30 206 71 95 0 176% 49% 5%
   Darth Vader 29428 121 4429 6222 2824 434 45 312 25 176 0 120% 62% 15%
   Biggs Darklighter 17406 108 4592 6217 716 30 218 82 139 10 244% 42% 0%
   Jedi Knight Guardian 26780 91 3623 2090 512 0 237 99 178 0 225% 53% 5%
   Ewok Elder 17829 116 4016 779 70 245 20 97 10 44% 48% 10%
   Lobot 14445 108 4606 266 180 239 10 181 56 70% 33% 0%
   Ima-Gun Di 26009 125 5184 8310 483 25 290 56 132 29 172% 57% 15%
   Hoth Rebel Scout 16950 149 5876 7830 592 55 203 102 117 5 122% 54% 0%
   HK-47 24883 103 4606 2560 480 40 257 49 213 0 145% 56% 10%
   Stormtrooper-1 16008 113 5393 690 0 199 75 120 0 162% 43% 0%
   Tusken Raider 28252 121 4780 7095 524 40 325 44 101 0 74% 44% 15%
   Ahsoka Tano 13534 93 4762 7578 1037 120 227 46 110 0 100% 20% 30%
   Cad Bane 13471 113 4137 6649 831 90 191 39 142 0 97% 38% 5%
   Teebo 26359 118 4154 6451 471 40 286 52 217 5 108% 44% 30%
   Coruscant Underworld Police 13812 106 4654 2879 749 80 189 36 318 0 27% 51% 5%
   Geonosian Soldier 15607 154 4880 7731 720 0 244 47 97 0 62% 45% 0%
   Nightsister Initiate 30724 114 4039 7477 6156 508 0 318 29 122 0 72% 47% 25%
   Greedo 13248 122 5477 2868 677 100 219 47 154 10 129% 42% 5%
   Mob Enforcer 23163 132 4036 3292 391 110 250 55 141 15 167% 51% 20%
   Kit Fisto 27347 120 3831 2804 551 10 281 56 153 5 130% 71% 15%
   Nightsister Acolyte 18540 147 3777 5893 368 280 157 10 133 45 92% 53% 0%
   Princess Leia 14399 164 4523 784 30 203 115 90 0 202% 51% 0%
   Qui-Gon Jinn 16540 151 4607 5696 7820 271 130 171 65 207 22 240% 52% 0%
   Ugnaught 15829 130 4696 2127 330 85 184 20 221 32 177% 59% 0%
   Admiral Ackbar 17354 119 4460 322 60 273 47 190 37 104% 57% 0%
   Nute Gunray 13147 150 6134 2111 834 0 198 94 86 0 164% 42% 10%
   Stormtrooper Han 17872 126 4345 717 50 259 60 100 0 109% 49% 15%
   Luke Skywalker 17168 119 5001 8376 888 10 226 54 58 0 92% 37% 10%
   Jedi Knight Anakin 21433 144 5080 4323 757 0 233 54 70 15 117% 58% 5%
   Lando Calrissian 16525 115 5039 3621 747 55 217 55 123 0 179% 54% 15%
   First Order Stormtrooper 26698 118 5956 428 20 352 36 201 0 42% 65% 5%
   First Order TIE Pilot 15465 128 7303 9764 919 10 210 65 60 0 42% 39% 0
   Resistance Pilot 16588 120 7781 7611 755 0 240 59 96 0 204% 39% 5%
   Resistance Trooper 15762 134 6818 8712 800 70 204 77 142 0 77% 58% 5%
   Kylo Ren 27972 122 3559 7940 3915 489 10 297 58 85 0 122% 45% 15%
   Finn 28998 119 5150 5638 446 20 354 29 167 5 62% 51% 25%
   Captain Phasma 25070 121 4451 2759 433 10 270 90 227 5 147% 70% 35%
   Poe Dameron 21255 150 4984 666 10 260 32 95 5 72% 72% 5%
   First Order Officer 15255 145 4772 7531 717 100 212 76 113 15 127% 51% 0%
   Rey 14312 172 7084 12044 10414 758 30 213 44 151 15 20% 50% 10%
   Grand Master Yoda 14809 163 5110 8223 4812 283 100 201 41 190 30 175% 56% 0%
   CT-7567 Rex 15234 140 4414 4644 668 65 182 77 171 0 77% 53% 5%
   General Grievous 14491 109 7066 3759 769 10 187 124 139 0 122% 48% 0%
"""

l = header.split('\n')
header_list = []
for t in l:
	if len(t)>0:
		header_list.append(t.strip().replace('-','_').replace(' ','_'))

l = data.split('\n')
name_list = []
hero_list = []
for t in l:
	if len(t.strip())>0:
		h=[]
		ll = t.split()
		name = ""
		for tt in ll:
			try:
				i = int(tt.replace('%',''))
				h.append(str(i))
			except ValueError:
				name += tt
		name_list.append(name)
		hero_list.append(h)

outfile=open('swgoh.sql','w')
outfile.write('CREATE TABLE stats(name text')
for t in header_list[1:]:
	outfile.write(','+t+' int')
outfile.write(');\n')

for i in range(len(hero_list)):
	outfile.write('INSERT INTO stats VALUES("'+name_list[i]+'"')
	for t in hero_list[i][:3]:
		outfile.write(','+t)
	for t in hero_list[i][-9:]:
		outfile.write(','+t)
	outfile.write(');\n')

outfile.close()
