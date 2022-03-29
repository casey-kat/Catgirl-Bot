import re
import syllables

# ------------------------------------------------------------------------------------------------------------------------------------------------

infile = open('./name_filter.txt', 'r')
name_filter = infile.read().replace('\n\n', '\n').splitlines()
infile.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# will check a sent message, and if it could be a valid troll or kid name (by following the letter count & syllable conventions) then it will reply saying so
async def name_check(message: str, isTest = False) -> str:
	# Troll Name
	name = find_name(message, first_word_length=6, second_word_length=6)
	if name and (isTest or name not in name_filter):
			name_array = name.split();
			# If the message contains two words - each of which are 6 letters long - send a message saying so, and return.
			if check_syllables(name_array[0], 1, False) and check_syllables(name_array[1], 1, False):
				return f'"{name.title()}" is a valid troll name'

	# Kid Name
	name = find_name(message, first_word_length=4, second_word_length=6, alt_second_word_length=7)
	if name and (isTest or name not in name_filter):
			name_array = name.split();
			# If the message contains two words - the first being 4 letters, the second being 6 or 7, and the second being 2 syllables - send a message saying so, and return.
			if check_syllables(name_array[0], 1, False) and check_syllables(name_array[1], 2, True):
				return f'"{name.title()}" is a valid kid name'

	return None


def find_name(message, first_word_length, second_word_length=None, alt_second_word_length=None) -> str:
    if second_word_length == None:
        second_word_length = first_word_length
    if alt_second_word_length == None:
        alt_second_word_length = second_word_length

    name = re.search(
        r'(?:\W|^)([a-zA-Z]{%i}) ([a-zA-Z]{%i,%i})(?:\W|$)'
        % (first_word_length, second_word_length, alt_second_word_length), message
    )

    if name:
        return name.group().strip().lower()


def check_syllables(name: str, minimum_syllables: int, must_be_equal: bool) -> bool:
	if must_be_equal and syllables.estimate(name) == minimum_syllables:
		return True
	elif syllables.estimate(name) >= minimum_syllables:
		return True
	return False


async def test():
	name_test_list = []
	
	for name in name_filter:
		if await name_check(name, isTest=True) is None:
			name_test_list.append(name)

	if len(name_test_list) > 0:
		#raise Exception('These canon names dont pass the test:', name_test_list)
		print('These canon names dont pass the test:', name_test_list)
		print('Homestuck module failed to load successfully')
		return

	print('Homestuck module loaded')