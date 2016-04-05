__version__ = '0.1.0'

class InvalidPassphraseLength(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

import urllib.request
import pathlib
import os
import random
import argparse

def generate_passphrase(length=6):
	if length < 6: raise InvalidPassphraseLength('passphrase length must be greater than 6 in order to generate a secure password')

	word_list = {}

	def download_and_parse():
		list_file = os.path.join(os.getcwd(), 'wordlist.asc')

		if not pathlib.Path(os.path.join(os.getcwd(), 'wordlist.asc')).is_file():
			print("Couldn't find word list. Downloading...")
			with urllib.request.urlopen('http://world.std.com/~reinhold/diceware.wordlist.asc') as response, open(list_file, 'wb') as out_file:
				data = response.read()
				out_file.write(data)
				print("Saved file to '%s'" % list_file)
				parse_list()
		else:
			parse_list()

	def parse_list():
		with open('wordlist.asc', 'rt') as f:
			for line in f:
				if not line: break
				if line.startswith("1") or line.startswith("2") or line.startswith("3") or line.startswith("4") or line.startswith("5") or line.startswith("6"):
					parts = line.strip().split('\t')
					index = int(parts[0])
					if not index in word_list:
						word_list[index] = parts[1]

	download_and_parse()

	if word_list:
		r = random.SystemRandom()
		result = []
		for i in range(0, length):
			word_index_array = []
			for j in range(5):
				word_index_array.append(r.randint(1, 6))
			word_index = int(''.join(str(x) for x in word_index_array))
			if word_index in word_list:
				result.append(word_list[word_index])
			else:
				print("Invalid key: %d" % word_index)
		return result

def main():
	arg_parser = argparse.ArgumentParser(prog='dicepyware', description='Generate cryptographically secure random passphrases for daily use. It uses the diceware method for generating the passphrases. Check out http://world.std.com/~reinhold/diceware.html for more info.')
	arg_parser.add_argument('-l', '--length', required=True, metavar='<passphrase length>', dest='passphrase_length', type=int, default=6, help='determine the passphrase length. Values lesser than 6 are considered invalid for generating a secure random password.')
	arg_parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
	args = arg_parser.parse_args()
	
	generated_passphrase = ' '.join(generate_passphrase(args.passphrase_length))
	print("Your generated passphrase: %s" % generated_passphrase)

if __name__ == "__main__":
	main()