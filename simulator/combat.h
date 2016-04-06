#include <stdio.h>
#include <stdlib.h>
#include "hero.h"
typedef struct {
	Hero* hero;
	float current_hp;
	int dodge_chance;
	int turn_meter;
	int speed;
	int id;
	int cooldown[5];
} Toon;

void attack(Toon* t1, Toon* t2);
void physicalDamage(Toon* t1, Toon* t2, float dmg);
void specialDamage(Toon* t1, Toon* t2, float dmg);

