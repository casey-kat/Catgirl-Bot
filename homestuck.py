import re
import syllables

# ------------------------------------------------------------------------------------------------------------------------------------------------

infile = open('./name_filter.txt', 'r')
names = infile.read().splitlines()
infile.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# will check a sent message, and if it could be a valid troll or kid name (by following the letter count & syllable conventions) then it will reply saying so
async def names_check(message):
    # If the message contains two words - each of which are 6 letters long - send a message saying so, and return.
	name = find_name(message.content, 6, 6)
	if name and check_name(name, 1, 1, False):
		await message.channel.send(f'"{name}" is a valid troll name')
		return
		
	# If the message contains two words - the first being 4 letters, the second being 6 or 7, and the second being 2 syllables - send a message saying so, and return.
	name = find_name(message.content, 4, 6, 7)
	if name and check_name(name, 1, 2, True):
		await message.channel.send(f'"{name}" is a valid kid name')
		return

def find_name(message, first_word, second_word=None, alt_second_word=None) -> str:
    if second_word == None:
        second_word = first_word
    if alt_second_word == None:
        alt_second_word = first_word

    name = re.search(
        r'(?:\W|^)([a-zA-Z]{%i}) ([a-zA-Z]{%i,%i})(?:\W|$)'
        % (first_word, second_word, alt_second_word), message
    )

    if name:
        return name.group().strip()


def check_name(name: str, first_syllables: int, second_syllables: int, must_be_equal: bool) -> bool:
    names = name.split()
    if must_be_equal:
        if name.lower() not in names and syllables.estimate(names[0]) == first_syllables and syllables.estimate(names[1]) == second_syllables:
            return True
    else:
        if name.lower() not in names and syllables.estimate(names[0]) > first_syllables and syllables.estimate(names[1]) > second_syllables:
            return True
    return False