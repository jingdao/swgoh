#include "combat.h"

#define disp(...) printf(__VA_ARGS__);gets(buffer);

char buffer[256];

void attack(Toon* t1, Toon* t2) {
	disp("%s attacks %s",t1->hero->name,t2->hero->name);
	if (rand() % 100 < t2->dodge_chance) {
		disp("%s DODGED the attack",t2->hero->name);
	} else {
		float dmg = rand() % (int)(t1->hero->max_damage[0]-t1->hero->min_damage[0]);
		dmg += t1->hero->min_damage[0];
		physicalDamage(t1,t2,dmg);
	}
}

void physicalDamage(Toon* t1, Toon* t2, float dmg) {
	float critChance = 0.05 + 1.0 / 1750 * t1->hero->phy_crit;
	if (1.0 * rand() / RAND_MAX < critChance) {
		dmg *= 1.5;
		disp("%s took %d damage (CRIT)",t2->hero->name,(int)dmg);
	} else {
		disp("%s took %d damage",t2->hero->name,(int)dmg);
	}
	t2->current_hp -= dmg;
	if (t1->hero->hp_steal > 0) {
		float gain = dmg * t1->hero->hp_steal;
		disp("%s gained %d health",t1->hero->name,(int)gain);
		t1->current_hp += gain;
		if (t1->current_hp > t1->hero->hp)
			t1->current_hp = t1->hero->hp;
	}

}

void specialDamage(Toon* t1, Toon* t2, float dmg) {
	float critChance = 0.05 + 1.0 / 1750 * t1->hero->sp_crit;
	if (1.0 * rand() / RAND_MAX < critChance) {
		dmg *= 1.5;
		disp("%s took %d damage (CRIT)",t2->hero->name,(int)dmg);
	} else {
		disp("%s took %d damage",t2->hero->name,(int)dmg);
	}
	t2->current_hp -= dmg;
	if (t1->hero->hp_steal > 0) {
		float gain = dmg * t1->hero->hp_steal;
		disp("%s gained %d health",t1->hero->name,(int)gain);
		t1->current_hp += gain;
		if (t1->current_hp > t1->hero->hp)
			t1->current_hp = t1->hero->hp;
	}
}
