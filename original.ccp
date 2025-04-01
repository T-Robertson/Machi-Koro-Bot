#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <fstream>

const int num_games = 100000;
const bool verbose_output = false;

//an enum for easy indexing
enum card{
	Wheat_Field,
	Ranch,
	Bakery,
	Cafe,
	Convenience_Store,
	Fruit_Veg_Market,
	Forest,
	Furniture_Factory,
	Apple_Orchard,
	Family_Restaurant,
	Station,
	Cheese_Factory,
	Stadium,
	Mine,
	TV_Station,
	Business_Center,
	Amusement_Park,
	Radio_Tower,
	Shopping_Mall
};

//some global variables about the game. Not very elegant, but it does the job.
int costs[19] = {1,1,1,2,2,2,3,3,3,3,4,5,6,6,7,8,16,22,10};
std::string names[19] = {"Wheat Field", "Ranch", "Bakery", "Cafe", "Convenience Store", "Fruit Veg Market", "Forest", "Furniture Factory", "Apple Orchard", "Family Restaurant", "Station", "Cheese Factory", "Stadium", "Mine", "TV Station", "Business Center", "Amusement Park", "Radio Tower", "Shopping Mall"};
std::vector<int> quantities = {6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6};
std::vector<std::vector<int>> activated_by_roll = {{},//0
												   {Wheat_Field},//1
												   {Ranch,Bakery},//2
												   {Cafe,Bakery},//3
												   {Convenience_Store},//4
												   {Forest},//5
												   {Stadium,TV_Station,Business_Center},//6
												   {Cheese_Factory},//7
												   {Furniture_Factory},//8
												   {Mine,Family_Restaurant},//9
												   {Apple_Orchard,Family_Restaurant},//10
												   {Fruit_Veg_Market},//11
												   {Fruit_Veg_Market}};//12

//The AI class. Again, not very elegant, but this is a quick throw-away program
class AI{
	std::vector<int> wanted_quantities;
	bool use_two_dice;

public:
	int money;
	std::string name;
	int wins;
	std::vector<int> owned_quantities;

	AI(std::vector<int> strat, bool two_dice, std::string Name)
	{
		wanted_quantities = strat;
		use_two_dice = two_dice;
		name = Name;
		
		wins = 0;
		reset();
	}
	
	void reset()
	{
		money = 3;
		owned_quantities = {1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	}
	
	bool roll_two_dice()
	{
		return use_two_dice && (owned_quantities[Station] == 1)  && (owned_quantities[Cheese_Factory] + owned_quantities[Furniture_Factory] + owned_quantities[Mine] + owned_quantities[Apple_Orchard] + owned_quantities[Fruit_Veg_Market]) > 0;
	}
	
	void action()
	{
		//go through our list of wanted_cards backwards to see what we can get
		int pick = -1;
		for (int i = 18; i >= 0; --i)
		{
			if (wanted_quantities[i] > owned_quantities[i] && costs[i] <= money && quantities[i] > 0)
			{
				pick = i;
				
				//if we don't own this yet, pick it! (if we do own it, we'll continue to see if there's another one we want but don't have
				if (owned_quantities[i] == 0)
					break;
			}
		}
		
		if (pick >= 0)
		{
			money -= costs[pick];
			--quantities[pick];
			++owned_quantities[pick];
			
			if (verbose_output)
				std::cout << "\tPlayer \"" << name << "\" bought a " << names[pick] << " for " << costs[pick] << " money\n";
		}
		else if (verbose_output)
		{
			std::cout << "\tPlayer \"" << name << "\" bought nothing\n";
		}
	}
	
	bool has_won()
	{
		return (owned_quantities[Station] + owned_quantities[Shopping_Mall] + owned_quantities[Amusement_Park] + owned_quantities[Radio_Tower] == 4);
	}
};

//some forward declarations
std::vector<AI*> create_bots();
void simulate_games(std::vector<AI*>& bots, int number_of_games);
void pay_out(std::vector<AI*>& bots, int current_player, int roll);
void cleanup_bots(std::vector<AI*>& bots);

int main()
{
	//seed the RNG (I should switch to the C++11 RNG, but this is more than adequate for a 6-sided die)
	std::srand(time(NULL));
	
	//create the bots
	std::vector<AI*> all_bots = create_bots();
	
	//set up the file stream for output
	std::ofstream outfile("data.txt");
	
	//which bot is the primary subject here
	int primary_bot = 0;
	for (unsigned opponent_bot_1 = 0; opponent_bot_1 < (all_bots.size() - 2); ++opponent_bot_1)
	{
		if (primary_bot == opponent_bot_1)
			continue;
		
		for (unsigned opponent_bot_2 = opponent_bot_1 + 1; opponent_bot_2 < (all_bots.size() - 1); ++opponent_bot_2)
		{
			if (primary_bot == opponent_bot_2)
				continue;
			
			for (unsigned opponent_bot_3 = opponent_bot_2 + 1; opponent_bot_3 < all_bots.size(); ++ opponent_bot_3)
			{
				if (primary_bot == opponent_bot_3)
					continue;
				
				std::vector<AI*> bots;
				bots.push_back(all_bots[primary_bot]);
				bots.push_back(all_bots[opponent_bot_1]);
				bots.push_back(all_bots[opponent_bot_2]);
				bots.push_back(all_bots[opponent_bot_3]);
				all_bots[primary_bot]->wins = 0;
				all_bots[opponent_bot_1]->wins = 0;
				all_bots[opponent_bot_2]->wins = 0;
				all_bots[opponent_bot_3]->wins = 0;
				
				simulate_games(bots,num_games);
				
				//spit out the data
				for (unsigned bot = 0; bot < bots.size(); ++bot)
					outfile << bots[bot]->name << "\t" << bots[bot]->wins << std::endl;
				outfile << std::endl;
			}
		}
	}
	
	//clean up the pointers
	cleanup_bots(all_bots);
	
	//return success
	return 0;
}

std::vector<AI*> create_bots()
{
	
	std::vector<int> card_baseline = {1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1};
	
	std::vector<int> BotStrat0 = card_baseline;
	BotStrat0[Ranch] = 6;
	BotStrat0[Cheese_Factory] = 2;
	AI* cheese_factory_bot = new AI(BotStrat0,true,"Cheese Factory");//http://boardgamegeek.com/thread/1291410/machi-koro-unbalanced
	
	std::vector<int> BotStrat1 = card_baseline;
	BotStrat1[Convenience_Store] = 6;
	BotStrat1[Bakery] = 3;
	AI* convenience_store_bot = new AI(BotStrat1,false,"Convenience Store");//http://boardgamegeek.com/thread/1263225/convenience-store-breaks-game-me-thinks
	
	std::vector<int> BotStrat2 = card_baseline;
	BotStrat2[Wheat_Field] = 2;
	BotStrat2[Ranch] = 2;
	BotStrat2[Forest] = 1;
	BotStrat2[Bakery] = 2;
	BotStrat2[Convenience_Store] = 2;
	BotStrat2[Cafe] = 2;
	BotStrat2[Family_Restaurant] = 1;
	BotStrat2[Stadium] = 1;
	AI* one_die_spread_bot = new AI(BotStrat2,false,"1 Die Spread");
	
	std::vector<int> BotStrat3 = card_baseline;
	BotStrat3[Bakery] = 6;
	AI* bakery_bot = new AI(BotStrat3,false,"Bakery");//http://boardgamegeek.com/thread/1263080/are-we-missing-something-shopping-mall-bakery-comb
	
	std::vector<int> BotStrat4 = card_baseline;
	BotStrat4[Forest] = 3;
	BotStrat4[Mine] = 3;
	BotStrat4[Furniture_Factory] = 2;
	AI* furniture_factory_bot = new AI(BotStrat4,true,"Furniture Factory");
	
	std::vector<int> BotStrat5 = card_baseline;
	BotStrat5[Wheat_Field] = 6;
	BotStrat5[Fruit_Veg_Market] = 6;
	AI* fruit_bot = new AI(BotStrat5,true,"Fruit & Veg Market");//http://boardgamegeek.com/thread/1157685/fruit-veg-blowout
	
	std::vector<int> BotStrat6 = card_baseline;
	BotStrat6[Wheat_Field] = 1;
	BotStrat6[Ranch] = 1;
	BotStrat6[Forest] = 1;
	BotStrat6[Mine] = 4;
	BotStrat6[Apple_Orchard] = 1;
	AI* mine_bot = new AI(BotStrat6,true,"Mines + Blue Spread");//http://boardgamegeek.com/thread/1077293/mines-why-would-i-buy-anything-else
	
	std::vector<int> BotStrat7 = card_baseline;
	BotStrat7[Wheat_Field] = 6;
	BotStrat7[Ranch] = 6;
	BotStrat7[Forest] = 1;
	AI* blue_one_die_bot = new AI(BotStrat7,false,"Blue 1 die");
	
	std::vector<AI*> all_bots;
	all_bots.push_back(cheese_factory_bot);
	all_bots.push_back(convenience_store_bot);
	all_bots.push_back(one_die_spread_bot);
	all_bots.push_back(bakery_bot);
	all_bots.push_back(furniture_factory_bot);
	all_bots.push_back(fruit_bot);
	all_bots.push_back(mine_bot);
	all_bots.push_back(blue_one_die_bot);
	
	return all_bots;
}

void simulate_games(std::vector<AI*>& bots, int number_of_games)
{
	for (int i = 0; i < number_of_games; ++i)
	{
		//play a game
		for (unsigned player = 0; player < bots.size(); ++player)
			bots[player]->reset();
		quantities = {6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6};
		
		for (unsigned player = std::rand() % bots.size(); ; player = (player + 1) % bots.size())
		{
			//first roll the dice
			int roll = (std::rand() % 6) + 1;
			if (bots[player]->roll_two_dice())
				roll += (std::rand() % 6) + 1;
				
			if (verbose_output)
				std::cout << "\tPlayer \"" << bots[player]->name << "\" rolled a " << roll << std::endl;
			
			//if this player has a Radio Tower then see if they want to reroll
			if (bots[player]->owned_quantities[Radio_Tower] == 1)
			{
				//get the list of buildings associated with this roll
				std::vector<int> for_this_roll = activated_by_roll[roll];
				
				//for each building in this list, see if the current player has any
				bool has_no_buildings = true;
				for (int b : for_this_roll)
				{
					if (bots[player]->owned_quantities[b] > 0)
					{
						has_no_buildings = false;
						break;
					}
				}
				
				//if the player doesn't have any activated buildings, then reroll
				if (has_no_buildings)
				{
					roll = (std::rand() % 6) + 1;
					if (bots[player]->roll_two_dice())
						roll += (std::rand() % 6) + 1;
					
					if (verbose_output)
						std::cout << "\tPlayer \"" << bots[player]->name << "\" rerolled a " << roll << std::endl;
				}
			}
			
			//distribute income
			pay_out(bots, player, roll);
			
			//finally, decide what the bot wants to do
			bots[player]->action();
			
			if (verbose_output)
			{
				std::cout << "\tPlayer Money:\n";
				
				for (unsigned p = 0; p < bots.size(); ++p)
					std::cout << "\t\t" << bots[p]->name << ": " << bots[p]->money << "\n";
			}
			
			//if a player won, then break out
			if (bots[player]->has_won())
			{
				++bots[player]->wins;
				break;
			}
		}
	}
}

void pay_out(std::vector<AI*>& bots, int player, int roll)
{
	//deal out money
	//	RED
	int& player_money = bots[player]->money;
	
	if (roll == 3 || roll == 9 || roll == 10)
	{
		for (unsigned p = 0; p < bots.size(); ++p)
		{
			if (p != player)
			{
				int boost = bots[p]->owned_quantities[Shopping_Mall];
				int total_to_take;
				if (roll == 3)
					total_to_take = (1 + boost) * bots[p]->owned_quantities[Cafe];
				else
					total_to_take = (2 + boost) * bots[p]->owned_quantities[Family_Restaurant];
				
				if (total_to_take > player_money)
					total_to_take = player_money;
					
				bots[p]->money += total_to_take;
				player_money -= total_to_take;
			}
		}
	}
	
	//	BLUE
	if (roll == 1 || roll == 2 || roll == 5 || roll == 9 || roll == 10)
	{
		int amount = 1;
		if (roll == 10)
			amount = 3;
		else if (roll == 9)
			amount = 5;
			
		int card = Apple_Orchard;
		if (roll == 1)
			card = Wheat_Field;
		else if (roll == 2)
			card = Ranch;
		else if (roll == 5)
			card = Forest;
		else if (roll == 9)
			card = Mine;
		
		for (unsigned p = 0; p < bots.size(); ++p)
			bots[p]->money += amount * bots[p]->owned_quantities[card];
	}
	
	//	GREEN & PURPLE
	int boost = bots[player]->owned_quantities[Shopping_Mall];
	switch (roll)
	{
		case 2: 
		case 3:	//Bakery
			player_money += (1 + boost) * bots[player]->owned_quantities[Bakery];
			break;
		case 4: //convenience store
			player_money += (3 + boost) * bots[player]->owned_quantities[Convenience_Store];
			break;
		case 6: //Stadium, TV Station, Business Center (ignoring that one for now)
			if (bots[player]->owned_quantities[Stadium] == 1)
			{
				for (unsigned p = 0; p < bots.size(); ++p)
				{
					if (p != player)
					{
						int total_to_take = 2;
						if (bots[p]->money < 2)
							total_to_take = bots[p]->money;
							
						bots[p]->money -= total_to_take;
						player_money += total_to_take;
					}
				}
			}
			if (bots[player]->owned_quantities[TV_Station] == 1)
			{
				//find the player with the most money
				int total_to_take = 5;
				int most_money = -1;
				unsigned player_to_take_from = 0;
				
				for (unsigned p = 0; p < bots.size(); ++p)
				{
					if (p != player && bots[p]->money > most_money)
					{
						most_money = bots[p]->money;
						player_to_take_from = p;
					}
				}
				
				if (bots[player_to_take_from]->money < 5)
					total_to_take = bots[player_to_take_from]->money;
				
				player_money += total_to_take;
				bots[player_to_take_from]->money -= total_to_take;
			}
			if (bots[player]->owned_quantities[Business_Center] == 1)
			{
				//do nothing for now, since none of the strategies use this card and it would be a pain
			}
			break;
		case 7: //Cheese Factory
			player_money += 3 * bots[player]->owned_quantities[Cheese_Factory] * bots[player]->owned_quantities[Ranch];
			break;
		case 8: //Furniture Factory
			player_money += 3 * bots[player]->owned_quantities[Furniture_Factory] * (bots[player]->owned_quantities[Forest] + bots[player]->owned_quantities[Mine]);
			break;
		case 11:
		case 12: //Fruit & Veg Market
			player_money += 2 * bots[player]->owned_quantities[Fruit_Veg_Market]  * (bots[player]->owned_quantities[Wheat_Field] + bots[player]->owned_quantities[Apple_Orchard]);
			break;
	}
}

void cleanup_bots(std::vector<AI*>& bots)
{
	for (AI* bot : bots)
		delete bot;
}
