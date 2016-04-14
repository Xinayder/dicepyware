# Copyright (C) 2016 Alexandre Oliveira
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see http://www.gnu.org/licenses/.

__version__ = '0.1.1'

# Imports
import re
import sys
import os
import random
import argparse

if (sys.version_info > (3, 0)):
	from urllib.request import urlopen  # Python 3
else:
	from urllib2 import urlopen			# Python 2

# Define Constants
SPECIAL_CHARS = r'''~!#$%^&*()-=+[]\{}:;"'<>?/0123456789'''
DICEWARE_WORDLIST = 'http://world.std.com/~reinhold/diceware.wordlist.asc'

def download_and_parse_word_list():

	# Define destination file for the word list.
	fp = os.path.join(os.getcwd(), 'wordlist.asc')

	# If the file does not exist already-- download and write it.
	if not os.path.isfile(os.path.join(os.getcwd(), 'wordlist.asc')):
		print("Couldn't find word list. Downloading...")
		with open(fp, 'wb') as fo:
			data = urlopen(DICEWARE_WORDLIST).read()
			fo.write(data)
			print("Saved file to '%s'." % fp)

	# Open the file and parse it.
	raw_word_list = ''
	with open(fp, 'r') as fi:
		raw_word_list = fi.read()
	return dict(re.findall(r'''^([1-6]{5})\t([\S]*)''', raw_word_list, re.MULTILINE))

def generate_passphrase(length=6, separator=' ', inc_special_character=False):

	# Evaluate input parameters for validity.
	if length < 6: raise ValueError('Passphrase length must be greater than 6 in order to generate a secure password.')
	if len(separator) > 1: raise ValueError('Separator can be, at most, one character long.')

	word_list = download_and_parse_word_list()
	if not word_list:
		raise IOError('Unable to open and parse word list.')

	# Generate a random seed.
	r = random.SystemRandom()

	# Roll for the word with the special character and the special character.
	spec_word = r.randint(0, length - 1)
	spec_char = SPECIAL_CHARS[(r.randint(1, 6) - 1) * 6 + (r.randint(1, 6) - 1)]

	# Define an empty list of results.
	result = []

	# Generate a number of words equal to the defined length.
	for i in range(0, length):

		# Randomly create a 5-digit string of integers 1-6.
		word_index = ''.join([str(r.randint(1, 6)) for j in range(5)])

		# If there is no associated word for the index, continue but complain.
		if word_index not in word_list:
			print("Invalid key: %d" % word_index)
			continue

		# Get word and insert the special character (at random) if appropriate.
		new_word = word_list.get(word_index)
		if inc_special_character and i == spec_word:
			new_word = list(new_word)
			new_word[r.randint(0, len(new_word) - 1)] = spec_char
			new_word = ''.join(new_word)

		# Append the word to the list of results.
		result.append(new_word)

	# Combine and return the list of results using the defined separator.
	return separator.join(result)

def main():
	arg_parser = argparse.ArgumentParser(prog='dicepyware', description='Generate cryptographically secure random passphrases for daily use. It uses the diceware method for generating the passphrases. Check out http://world.std.com/~reinhold/diceware.html for more info.')
	arg_parser.add_argument('-l', '--length', required=False, metavar='<passphrase length>', dest='passphrase_length', type=int, default=6, help='determine the passphrase length. Values lesser than 6 are considered invalid for generating a secure random password.')
	arg_parser.add_argument('-s', '--separator', required=False, metavar='<word seperator>', dest='separator', type=str, default=' ', help='declare the character separator between each word.  Default is ` `.')
	arg_parser.add_argument('-c', '--special', required=False, dest='inc_special_character', default=False, action='store_true', help='include a random character.')
	arg_parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
	args = arg_parser.parse_args()

	generated_passphrase = generate_passphrase(
		length=args.passphrase_length,
		separator=args.separator,
		inc_special_character=args.inc_special_character
	)
	print("Your generated passphrase: %s" % generated_passphrase)

if __name__ == "__main__":
	main()
