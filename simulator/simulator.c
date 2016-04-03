#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>
#include "hero.h"
#define RED "\033[0;31m"
#define GREEN "\033[0;32m"
#define ORANGE "\033[0;33m"
#define BLUE "\033[0;34m"
#define PURPLE "\033[0;35m"
#define CYAN "\033[0;36m"
#define GRAY "\033[0;37m"
#define YELLOW "\033[1;33m"
#define WHITE "\033[1;37m"
#define NORMAL "\033[0m"
#define ROSTER_SIZE sizeof(ROSTER)/sizeof(Hero*)

typedef struct {
	Hero* hero;
	float current_hp;
	int turn_meter;
	int speed;
	int id;
} Toon;

void displayHero(Toon* toons,int n) {
	for (int i=0;i<n;i++)
		printf("%-11.11s ",toons[i].hero->name);
	printf("\n");
	for (int i=0;i<n;i++) {
		if (toons[i].current_hp <= 0)
			printf("%s%5d/%5d%s ",WHITE,0,(int)toons[i].hero->hp,NORMAL);
		else if (toons[i].current_hp >= toons[i].hero->hp / 2)
			printf("%s%5d/%5d%s ",GREEN,(int)toons[i].current_hp,(int)toons[i].hero->hp,NORMAL);
		else
			printf("%s%5d/%5d%s ",RED,(int)toons[i].current_hp,(int)toons[i].hero->hp,NORMAL);
	}
	printf("\n");
	printf(CYAN);
	for (int i=0;i<n;i++) {
		for (int j=0;j<=1000;j+=100) {
			if (toons[i].turn_meter >= j)
				printf("=");
			else
				printf(" ");
		}
		printf(" ");
	}
	printf(NORMAL);
	printf("\n");
}

void shuffleTeam(Toon* my_team, Toon* enemy_team, int n) {
	int index[ROSTER_SIZE];
	for (int i=0;i<ROSTER_SIZE;i++)
		index[i] = i;
	for (int i=0;i<n*2;i++) {
		int j = rand() % (ROSTER_SIZE - i);
		int tmp = index[j];
		index[j] = index[ROSTER_SIZE - 1 - i];
		index[ROSTER_SIZE - 1 - i] = tmp;
	}
	for (int i=0;i<n;i++) {
		int j = index[ROSTER_SIZE - 1 - i];
		my_team[i].hero = ROSTER[j];
	}
	for (int i=0;i<n;i++) {
		int j = index[ROSTER_SIZE - 1 - n - i];
		enemy_team[i].hero = ROSTER[j];
	}
}

void initializeTeam(Toon* my_team,Toon* enemy_team,int n) {
	for (int i=0;i<n;i++) {
		my_team[i].current_hp = my_team[i].hero->hp;
		my_team[i].speed = my_team[i].hero->speed;
		my_team[i].turn_meter = 0;
		my_team[i].id = i;
	}
	for (int i=0;i<n;i++) {
		enemy_team[i].current_hp = enemy_team[i].hero->hp;
		enemy_team[i].speed = enemy_team[i].hero->speed;
		enemy_team[i].turn_meter = 0;
		enemy_team[i].id = i + n;
	}

}

void generateUnitList(Toon** units,Toon* my_team,Toon* enemy_team,int* my_team_size,int* enemy_team_size) {
	int m = *my_team_size;
	int n = *enemy_team_size;
	*my_team_size = 0;
	*enemy_team_size = 0;
	for (int i=0;i<m;i++) {
		if (my_team[i].current_hp > 0) {
			Toon* t = my_team + i;
			int j = (*my_team_size)++;
			units[j] = t;
		} else {
			memmove(my_team+i,my_team+i+1,sizeof(Toon)*(m-1-i));
			i--;
			m--;
		}
	}
	for (int i=0;i<n;i++) {
		if (enemy_team[i].current_hp > 0) {
			Toon* t = enemy_team + i;
			int j = *my_team_size + (*enemy_team_size)++;
			units[j] = t;
		} else {
			memmove(enemy_team+i,enemy_team+i+1,sizeof(Toon)*(n-1-i));
			i--;
			n--;
		}
	}
}

int compareTurnMeter(const void* a,const void* b) {
	Toon* t1 = *(Toon**)a;
	Toon* t2 = *(Toon**)b;
	if (t1->turn_meter == t2->turn_meter)
		return (rand()%2) * 2 - 1;
	return t2->turn_meter - t1->turn_meter;
}

int getTurnOrder(Toon** units,int n) {
	static int turnOrder[10];
	static int l=0;
	while (l > 0) {
		l--;
		for (int i=0;i<n;i++)
			if (units[i]->id == turnOrder[l])
				return i;
	}
	Toon* queue[20];
	memcpy(queue,units,n*sizeof(Toon*));
	while (true) {
		int maxTurnMeter = 0;
		for (int i=0;i<n;i++)
			if (units[i]->turn_meter > maxTurnMeter)
				maxTurnMeter = units[i]->turn_meter;
		if (maxTurnMeter > 1000)
			break;
		for (int i=0;i<n;i++)
			units[i]->turn_meter += units[i]->speed;
	}
	qsort(queue,n,sizeof(Toon*),compareTurnMeter);
	for (int i=n-1;i>=0;i--)
		if (queue[i]->turn_meter > 1000)
			turnOrder[l++] = queue[i]->id;
	return turnOrder[--l];
}

int main(int argc,char* argv[]) {
	srand(time(NULL));
//	srand(0);
	Toon my_team[5];
	Toon enemy_team[5];
	Toon* units[10];
	shuffleTeam(my_team,enemy_team,5);
	initializeTeam(my_team,enemy_team,5);
	int my_team_size = 5, enemy_team_size = 5;
	generateUnitList(units,my_team,enemy_team,&my_team_size,&enemy_team_size);

	for (int i=0;i<10;i++) {
		int turn = getTurnOrder(units,my_team_size+enemy_team_size);
//		displayHero(my_team,5);
//		displayHero(enemy_team,5);
		units[turn]->turn_meter -= 1000;
		printf("%s %d\n",units[turn]->hero->name,units[turn]->speed);
	}

}
