import json
import random 
import pprint

deck_list = ['Baral, Chief of Compliance', 'Baral, Chief of Compliance', 'Baral, Chief of Compliance', 'Baral, Chief of Compliance', 'Goblin Electromancer', 'Goblin Electromancer', 'Desperate Ritual', 'Desperate Ritual', 'Desperate Ritual', 'Desperate Ritual', 'Gifts Ungiven', 'Gifts Ungiven', 'Gifts Ungiven', 'Gifts Ungiven', 'Grapeshot', 'Grapeshot', 'Grapeshot', 'Manamorphose', 'Manamorphose', 'Manamorphose', 'Manamorphose', 'Noxious Revival', 'Opt', 'Opt', 'Opt', 'Opt', 'Past in Flames', 'Past in Flames', 'Pyretic Ritual', 'Pyretic Ritual', 'Pyretic Ritual', 'Pyretic Ritual', 'Remand', 'Remand', 'Remand', 'Serum Visions', 'Serum Visions', 'Serum Visions', 'Serum Visions', 'Sleight of Hand', 'Sleight of Hand', 'Sleight of Hand', 'Sleight of Hand', 'Island', 'Island', 'Island', 'Mountain', 'Shivan Reef', 'Shivan Reef', 'Shivan Reef', 'Shivan Reef', 'Snow-Covered Island', 'Spirebluff Canal', 'Spirebluff Canal', 'Spirebluff Canal', 'Spirebluff Canal', 'Steam Vents', 'Steam Vents', 'Steam Vents', 'Steam Vents']

shuffled_deck = []

shuffled_deck.append(random.sample(deck_list, len(deck_list)))

stack = []

card_structure = {'Land': ['type', 'text'], 'Creature': ['manaCost', 'types', 'text'], 'Planeswalker': ['manaCost', 'types', 'text'], 'Enchantment': ['manaCost', 'types', 'text'], 'Sorcery': ['manaCost', 'types', 'text'], 'Instant': ['manaCost', 'types', 'text']}

battlefield = {'Land': [], 'Creature': [], 'Artifact': [], 'Enchantment': [], 'Planeswalker': []}

life_total = 20

all_the_cards = {}

hand_list = ['Manamorphose', 'Pyretic Ritual', 'Noxious Revival', 'Remand', 'Opt', 'Serum Visions', 'Gifts Ungiven']

graveyard_list = ['Past in Flames', 'Opt', 'Serum Visions', 'Pyretic Ritual', 'Steam Vents']

mana_pool = {'R': 2, 'W': 0, 'U': 1, 'B': 0, 'G': 0, 'C': 0}

with open('/Users/darrylhoard/Documents/AllCards.json') as f:
	all_the_cards = json.load(f)

def card_resolution(card_name, starting_list, ending_list, list_of_cards):
	global stack
	print(f'{card_name} Effects:')
	card_effects[card_name](starting_list, ending_list, list_of_cards)
	stack.pop(0)
	
def stack_add(card_name, current_list, ending_list, list_of_cards):
	stack.insert(0, card_name)
	current_list.remove(card_name)
	print(f'{card_name} has been added to the stack.')
	print(stack)
	print('Would you like to respond?')
	response = input()
	if response.lower() in ['y', 'yes', 'sure', 'yea']:
		global hand_list
		print('\n')
		display_horizontal(hand_list)
		print('What would you like to do?')
		focus = input()
		if focus in hand_list:
			create_card([focus])
			if all_the_cards[focus]['types'][0] == 'Land':
				print('Back(B)'.rjust(16))
				focus_choice = input()
				if focus_choice.lower() in ['back', 'b']:
					stack.remove(card_name)
					current_list.append(card_name)
					stack_add(card_name, current_list)
			else:
				if all_the_cards[focus]['types'][0] == 'Instant':
					print('Options: Cast(C)\n')
					print('Back(B)'.rjust(16))
					focus_choice = input()
					if focus_choice.lower() in ['cast', 'c']:
						print(stack)
						current_card_cost(focus)
					elif focus_choice.lower() in ['back', 'b']:
						stack.remove(card_name)
						current_list.append(card_name)
						stack_add(card_name, current_list, ending_list, list_of_cards)
				elif 'Flash' in all_the_cards[focus]['text']:
					print('Options: Cast(C)\n')
					print('Back(B)'.rjust(16))
					focus_choice = input()
					if focus_choice.lower() in ['cast', 'c']:
						print(stack)
						current_card_cost(focus)
					elif focus_choice.lower() in ['back', 'b']:
						stack.remove(card_name)
						current_list.append(card_name)
						stack_add(card_name, current_list, ending_list, list_of_cards)
				else:
					print('Back(B)'.rjust(16))
					focus_choice = input()
					if focus_choice.lower() in ['back', 'b']:
						stack.remove(card_name)
						current_list.append(card_name)
						stack_add(card_name, current_list, ending_list, list_of_cards)
	else:
		for i in stack:
			card_resolution(i, current_list, ending_list, list_of_cards)
		hand_main_menu()




def current_card_cost(card_name):
	""" Splits mana cost into a dictionary of generic and colored costs"""
	card_specs = {}
	full_cost = all_the_cards[card_name]['manaCost']
	full_cost = full_cost[1:-1]
	split_cost = full_cost.split("}{")
	if split_cost[0].isdigit():
		color_cost = split_cost[1:]
		for i in range(len(color_cost)):
			color_cost[i] = color_cost[i].split('/')
		card_specs[card_name] = {'Generic': int(split_cost[0]), 'Colored Cost': color_cost}
	else: 
		for i in range(len(split_cost)):
			split_cost[i] = split_cost[i].split('/')
		card_specs[card_name] = {'Generic': '', 'Colored Cost': split_cost}
	"""Reduces generic cost if applicable """
	cast_cost = card_specs[card_name]
	if cast_cost['Generic'] not in  [0, '']:
		if all_the_cards[card_name]['type'] in ['Sorcery', 'Instant']:
			for i in battlefield['Creature']:
				if i in ['Baral, Chief of Compliance', 'Goblin Electromancer']:
					cast_cost['Generic'] = cast_cost['Generic'] - 1
					if cast_cost['Generic'] < 0:
						cast_cost['Generic'] = 0
	print(f'Current Casting Cost: {cast_cost}')
	print('Would you like to cast this card?')
	choice = input()
	if choice.lower() in ['y', 'yes']:
		cast_a_card(card_specs, card_name)

	else:
		hand_main_menu()
			
def cast_a_card(card_dictionary, card_name):
	global mana_pool
	global life_total
	global hand_list
	global graveyard_list
	amount_paid = {'Generic': 0 , 'Colored Cost': []}
	card_cost = {}
	for k, v in card_dictionary[card_name].items():
		card_cost[k] = v 
	undo_dictionary = {'R': 0, 'W': 0, 'U': 0, 'B': 0, 'G': 0, 'C': 0}
	print(card_dictionary)
	if str(card_dictionary[card_name]['Generic']).isdigit():
		while (amount_paid['Generic'] < card_dictionary[card_name]['Generic']):
			print('What color would you like to use to pay the generic cost?')
			generic_choice = input()
			print('How much of your this color would you like to spend?')
			amount_of_color = int(input())
			if amount_of_color <= mana_pool[generic_choice]:
				if amount_of_color <= card_dictionary[card_name]['Generic']:
					card_cost['Generic'] = card_cost['Generic'] - amount_of_color
					mana_pool[generic_choice] = mana_pool[generic_choice] - amount_of_color
					amount_paid['Generic'] = amount_paid['Generic'] + amount_of_color
					undo_dictionary[generic_choice] = undo_dictionary[generic_choice] + amount_of_color
		print(amount_paid)
		print(card_cost)
		print(undo_dictionary)
		print(card_dictionary)
		print(mana_pool)
		for i in card_dictionary[card_name]['Colored Cost']:
			if len(i) == 1:
				for k in mana_pool.keys():
					if k in i: 
						if mana_pool[k] > 0:
							amount_paid['Colored Cost'].append([k])
							mana_pool[k] = mana_pool[k] - 1
							undo_dictionary[k] = undo_dictionary[k] + 1 
						else: 
							print(f'You do not have enough {k} in your mana pool. Back(b)')
							back_choice = input()
							for k in undo_dictionary.keys():
									mana_pool[k] = mana_pool[k] + undo_dictionary[k]
									print(mana_pool)
							if back_choice.lower() in ['back','b']:
									hand_main_menu()


			else:
				print(i)
				print('How would you like to pay this cost?')
				color_choice = input()
				if color_choice in i:
					if color_choice.lower() in ['p']:
						if life_total > 2:
							amount_paid['Colored Cost'].append([color_choice])
							life_total = life_total - 2
							print(f'Life Total: {life_total}') 
						else: 
							print('You cannot pay this cost this way.')
					else:	
						if color_choice in i:
							if mana_pool[color_choice] > 0:
								amount_paid['Colored Cost'].append([color_choice])
								mana_pool[color_choice] = mana_pool[color_choice] - 1
								undo_dictionary[color_choice] = undo_dictionary[color_choice] + 1 
							else:
								back_choice = input()
								for k in undo_dictionary.keys():
										mana_pool[k] = mana_pool[k] + undo_dictionary[k]
										print(mana_pool)
								print(f'You do not have enough {color_choice} in your mana pool.')
								if back_choice.lower() in ['back','b']:
									hand_main_menu()
				else: 
					print('Not a valid selection.')
					current_card_cost(card_name)

		print(f'Mana Pool: {mana_pool}')
		print(f'Is this how you would like to pay the cost? {amount_paid}')
		cost_answer = input()
		if cost_answer.lower() in ['yes', 'yep', 'y', 'sure']:
			card_name_list = [card_name]
			stack_add(card_name, hand_list, graveyard_list, card_name_list)
		else:
			print('Back(b)')
			back_choice = input()
			for k in undo_dictionary.keys():
				mana_pool[k] = mana_pool[k] + undo_dictionary[k]
				print(mana_pool)
			if back_choice.lower() in ['back','b']:
				hand_main_menu()
			
	else:
		for i in card_dictionary[card_name]['Colored Cost']:
			if len(i) == 1:
				for k in mana_pool.keys():
					if k in i: 
						if mana_pool[k] > 0:
							amount_paid['Colored Cost'].append([k])
							mana_pool[k] = mana_pool[k] - 1
							undo_dictionary[k] = undo_dictionary[k] + 1
						else:
							print(f'You do not have enough {k} in your mana pool. Back(b)')
							back_choice = input()
							for k in undo_dictionary.keys():
									mana_pool[k] = mana_pool[k] + undo_dictionary[k]
									print(mana_pool)
							if back_choice.lower() in ['back','b']:
									hand_main_menu()


			else:				
				print(i)
				print('How would you like to pay this cost?')
				color_choice = input()
				if color_choice.lower() in ['p']:
					if life_total > 2:
						amount_paid['Colored Cost'].append([color_choice])
						life_total = life_total - 2
						print(f'Life Total: {life_total}') 
					else: 
						print('You cannot pay this cost this way.')
				else:	
					if color_choice in i:
						if mana_pool[color_choice] > 0:
							amount_paid['Colored Cost'].append([color_choice])
							mana_pool[color_choice] = mana_pool[color_choice] - 1
							undo_dictionary[color_choice] = undo_dictionary[color_choice] + 1
						else:
							print(f'You do not have enough {k} in your mana pool. Back(b)')
							back_choice = input()
							for k in undo_dictionary.keys():
									mana_pool[k] = mana_pool[k] + undo_dictionary[k]
									print(mana_pool)
							if back_choice.lower() in ['back','b']:
									hand_main_menu()

		print(f'Mana Pool: {mana_pool}')
		print(f'Is this how you would like to pay the cost? {amount_paid}')
		cost_answer = input()
		if cost_answer.lower() in ['yes', 'yep', 'y', 'sure']:
			card_name_list = [card_name]
			print(card_name_list)
			stack_add(card_name, hand_list, graveyard_list, card_name_list)
		else:
			print('Back(b)')
			back_choice = input()
			for k in undo_dictionary.keys():
				mana_pool[k] = mana_pool[k] + undo_dictionary[k]
				print(mana_pool)
			if back_choice.lower() in ['back','b']:
				hand_main_menu()


def create_card(cards_to_display):
	for i in cards_to_display:
		exact_card = all_the_cards[i]['name']
		card_type = all_the_cards[i]['types'][0]
		print('________________________________')
		print(exact_card, end = '   ')
		if exact_card in ['Mountain', 'Island', 'Forest', 'Swamp', 'Plains', 'Waste']:
			print('\n')
			print('\n')
			print(all_the_cards[i]['type'])
			print('__________________________________')
		else: 
			for i in card_structure[card_type]:
				print(all_the_cards[exact_card][i])
				print('\n')
			if card_type == 'Creature':
				power = all_the_cards[exact_card]['power']
				toughness = all_the_cards[exact_card]['toughness']
				print(f'{power}/{toughness}'.rjust(30))
			elif card_type == 'Planeswalker':
				loyalty = all_the_cards[exact_card]['loyalty']
				print(f'L: {loyalty}'.rjust(30))
			print('__________________________________')

def display_horizontal(cards_to_display):
	for i in cards_to_display:
		exact_card = all_the_cards[i]['name']
		""" Bug below, if first and last name in list are the same,
		after the first printing, a new line will be created."""
		if i == cards_to_display[len(cards_to_display) - 1]:
			if 'manaCost' in all_the_cards[i]:
				mana_cost = all_the_cards[i]['manaCost']
				print(f'|{exact_card}', end=f'       {mana_cost}|\n')
			else:
				print(f'|{exact_card}', end='        |\n')
		else:
			if 'manaCost' in all_the_cards[i]:
				mana_cost = all_the_cards[i]['manaCost']
				print(f'|{exact_card}', end=f'          {mana_cost}|')
			else: 
				print(f'|{exact_card}', end='        |')

def zone_transfer(starting_list, ending_list, list_of_cards):
	global hand_list
	global graveyard_list
	for i in list_of_cards:
		if i in starting_list:
			ending_list.append(i) 
			starting_list.remove(i)

def zone_transfer_1(starting_list, ending_list, list_of_cards):
	global hand_list
	global graveyard_list
	for i in list_of_cards:
		if i in starting_list:
			ending_list.append(i) 
			starting_list.remove(i)
	hand_main_menu()

def search_your_library(valid_targets, number_of_cards, unique):
	loop_control = 0
	search_target = []
	while (loop_control < 1):
		for i in shuffled_deck[0]:
			print([i])
		print("To conclude search, enter 'Done'.")
		for i in range(number_of_cards):
			p = i + 1
			print(f'Enter card choice {p}/{number_of_cards}:')
			selected_card = input()
			if selected_card.lower() != 'done':
				if selected_card in shuffled_deck[0]:
					if all_the_cards[selected_card]['types'][0] in valid_targets:
						if unique.lower() == 'yes':
							if selected_card not in search_target:
								search_target.append(selected_card)
							else:
								print('Not A Valid Selection.')
						else: 
							search_target.append(selected_card)
					else:
						print('Not A Valid Selection.')
				else: 
					print('Not A Valid Selection.')
			else:
				break
		print(f'Confirm Search Target(s)? Enter Yes(y) or No(n): {search_target}')
		response = input()
		if response.lower() in ['yes', 'y']:
			for i in search_target:
				shuffled_deck[0].remove(i)
			return search_target
			loop_control = loop_control + 1
		elif response.lower() in ['no', 'n']:
			search_target.clear()
			continue
		elif response.lower() == 'read':
			create_card(search_target)
			search_target.clear()
			continue
		else:
			search_target.clear()
			continue

def scry(x):
	global shuffled_deck
	saved_deck = shuffled_deck
#	for i in range(len(shuffled_deck)):
#		saved_deck.append(shuffled_deck[i])
	scryed_cards = saved_deck[0][0:x]
	while len(scryed_cards) > 0:
		print('Scryed Cards:')
		print(scryed_cards)
		if len(scryed_cards) == 1:
			scry_choice = scryed_cards[0]
			print('Top or Bottom?')
			top_bottom_choice = input()
			if top_bottom_choice.lower() == 'bottom':
				for i in range(len(scryed_cards)):
					entry_index = int(saved_deck[0].index(scry_choice))
				saved_deck.append(saved_deck[0].pop(entry_index))
				scryed_cards.remove(scry_choice)
				continue
			elif top_bottom_choice.lower() == 'top':
				for i in range(len(scryed_cards)):
					entry_index = int(saved_deck[0].index(scry_choice))
				saved_deck[0].insert(0, saved_deck[0].pop(entry_index))
				scryed_cards.remove(scry_choice)
				continue
		else:
			print('Which card would you like to scry?')
			scry_choice = input()
			if scry_choice in scryed_cards:
				print('Top or Bottom?')
				top_bottom_choice = input()
				if top_bottom_choice.lower() == 'bottom':
					for i in range(len(scryed_cards)):
						entry_index = int(saved_deck[0].index(scry_choice))
					saved_deck.append(saved_deck[0].pop(entry_index))
					scryed_cards.remove(scry_choice)
					continue
				elif top_bottom_choice.lower() == 'top':
					for i in range(len(scryed_cards)):
						entry_index = int(saved_deck[0].index(scry_choice))
					saved_deck[0].insert(0, saved_deck[0].pop(entry_index))
					scryed_cards.remove(scry_choice)
					continue
	

def draw_card(number):
	global shuffled_deck
	for i in range(number):
		hand_list.append(shuffled_deck[0].pop(0))
	return hand_list[len(hand_list) - 1]

def noxious_revival(starting_list, ending_list, list_of_cards):
	global graveyard_list
	global shuffled_deck
	print('\n')
	print('Graveyard')
	print('___________________')
	for i in graveyard_list:
		print(i)
	print('\n')
	print('Enter card name in Graveyard to move to the top of your library:')
	revival_choice = input()
	if revival_choice in graveyard_list:
		graveyard_list.remove(revival_choice)
		shuffled_deck[0].insert(0, revival_choice)

def serum_visions(starting_list, ending_list, list_of_cards):
	drawn_card = draw_card(1)
	print(f'You have drawn: {drawn_card}')
	print('Hand:', end=' ')
	display_horizontal(hand_list)
	scry(2) 
	

def past_in_flames(starting_list, ending_list, list_of_cards):
	for i in graveyard_list:
		if all_the_cards[i]['type'] in ['Instant', 'Sorcery']:
			flashback_cost = all_the_cards[i]['manaCost']
			print(f'{i} Flashback Cost{flashback_cost}')
		else: 
			print(i)


def opt(starting_list, ending_list, list_of_cards):
	scry(1)
	drawn_card = draw_card(1)
	print(f'You have drawn: {draw_card}')
	print('Hand:', end=' ')

def gifts_ungiven(starting_list, ending_list, list_of_cards):
	opponent_choice = []
	all_type_search = ['Creature', 'Instant', 'Enchantment', 'Planeswalker', 'Sorcery', 'Land', 'Artifact']
	print('')
	gift_pile = search_your_library(all_type_search, 4, 'yes')
	print(f'Opponent Chooses 2 Cards to Put into the Graveyard From: {gift_pile}')
	for i in range(2):
		print("Opponent's Choice:")
		opponent_choice.append(input())
		print('\n')
	zone_transfer(gift_pile, graveyard_list, opponent_choice)
	if gift_pile != []:
		zone_transfer(gift_pile, hand_list, gift_pile)
	print('Cards in Graveyard:')
	for i in graveyard_list:
		print(i)

def sleight_of_hand(starting_list, ending_list, list_of_cards):
	looked_cards = []
	zone_transfer(shuffled_deck, looked_cards, shuffled_deck[0:2])
	print(looked_cards)
	while len(looked_cards) > 0:
		print('Looking at:')
		print(looked_cards)
		print('Which card would you like to put into your hand?')
		look_choice = input()
		zone_transfer(looked_cards, hand_list, [look_choice])
		zone_transfer(looked_cards, shuffled_deck, looked_cards)
	print('Hand:', end=' ')
		
def pyretic_ritual(starting_list, ending_list, list_of_cards):
	mana_pool['R'] = mana_pool['R'] + 3
	pprint.pprint(mana_pool)
	
def remand(starting_list, ending_list, list_of_cards):
	global stack
	print('Which spell would you like to counter?')
	c = 0 
	for i in stack:
		print(f'{i} : [{c}]')
		c = c + 1
	response = input()
	if response.isdigit():
		if int(response) <= len(stack):
			stack.pop(int(response))
	draw_card(1)


def desperate_ritual(starting_list, ending_list, list_of_cards):
	mana_pool['R'] = mana_pool['R'] + 3
	pprint.pprint(mana_pool)

def manamorphose(starting_list, ending_list, list_of_cards):
	for i in range(2):
		print('Which color would you like to add mana for?')
		color_choice = input()
		if color_choice.lower() in ['red', 'r']:
			mana_pool['R'] += 1
		elif color_choice.lower() in ['blue', 'u']:
			mana_pool['U'] += 1
		elif color_choice.lower() in ['white', 'w']:
			mana_pool['W'] += 1
		elif color_choice.lower() in ['black', 'b']:
			mana_pool['B'] += 1
		elif color_choice.lower() in ['green', 'g']:
			mana_pool['G'] += 1
	draw_card(1)
	pprint.pprint(mana_pool)
	print('Hand:', end=' ')

def hand_main_menu():
	global hand_list
	print('\n')
	display_horizontal(hand_list)
	print('What would you like to do?')
	focus = input()
	if focus in hand_list:
		create_card([focus])
		if all_the_cards[focus]['types'][0] == 'Land':
			print('Options: Play(P)\n')
			print('Back(B)'.rjust(16))
			focus_choice = input()
			if focus_choice.lower() in ['play', 'p']:
				zone_transfer(hand_list, battlefield['Land'], [focus])
				print('\n')
				print('Lands:', end='  ')
				display_horizontal(battlefield['Land'])
				print('____________________________________________________________________________________')
				print('Cards in Hand:', end='  ')
				display_horizontal(hand_list)
			elif focus_choice.lower() in ['back', 'b']:
				hand_main_menu()
		else:
			print('Options: Cast(C)\n')
			print('Back(B)'.rjust(16))
			focus_choice = input()
			if focus_choice.lower() in ['cast', 'c']:
				current_card_cost(focus)
			elif focus_choice.lower() in ['back', 'b']:
				hand_main_menu()
	elif focus.lower() == 'view lands':
		print('Lands:', end='  ')
		display_horizontal(battlefield['Land'])
		print('Type Back(B) to return to hand:')
		if input().lower() in ['back', 'b']:
			hand_main_menu()

	elif focus.lower() == 'view deck':
		global shuffled_deck
		pprint.pprint(shuffled_deck)
		print('Type Back(B) to return to hand:')
		if input().lower() in ['back', 'b']:
			hand_main_menu()

	elif focus.lower() == 'view graveyard':
		print('Graveyard:')
		display_horizontal(graveyard_list)
		print('Type Back(B) to return to hand:')
		if input().lower() in ['back', 'b']:
			hand_main_menu()

	elif focus.lower() == 'view mana pool':
		print(mana_pool)
		print('Back(b)')
		back_choice = input()
		if back_choice.lower() in ['back','b']:
			hand_main_menu()

	elif focus.lower() == 'exit':
		quit()
	else:
		print('Not a valid option.')
		hand_main_menu()

card_effects = {'Remand': remand, 'Serum Visions': serum_visions,'Pyretic Ritual': pyretic_ritual, 'Desperate Ritual': desperate_ritual, 'Sleight of Hand': sleight_of_hand, 'Manamorphose': manamorphose, 'Gifts Ungiven': gifts_ungiven, 'Past in Flames': past_in_flames, 'Opt': opt, 'Noxious Revival': noxious_revival}

hand_main_menu()
