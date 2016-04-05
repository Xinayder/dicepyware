# dicepyware

dicepyware is an utility that generates cryptographically secure and random passphrases for your daily use. It utilizes the [Diceware method][diceware] for picking words from a list.

Python version: 3.4.x or newer.

### Usage
`python dicepyware.py -l <length>`
Passing a length lesser than 6 will raise an error.

### FAQ

**Why can't I generate smaller passphrases?**
According to their [FAQ][diceware-faq], a 4-word passphrase only provides *51.6 bits* of entropy, almost the same number of bits as an 8 random ASCII character password.
Five word passphrases also are not allowed because they are easily breakable by a powerful botnet.

If you're looking for true secure passphrases, consider using a length of 8 words or more.


[diceware]: http://world.std.com/~reinhold/diceware.html
[diceware-faq]: http://world.std.com/~reinhold/dicewarefaq.html