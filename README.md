# dicepyware

dicepyware is a Python utility that generates cryptographically secure and random passphrases for your daily use. It utilizes the [Diceware method][diceware] for picking words from a list.

Python version required: 3.4.4 or newer.

### Usage
`python dicepyware.py [-l <length>] [-s <separator>] [-c]`

- `l`: Number of words to include.  (default: `6`; minimum: `6`)
- `s`: The separator character to use between each word.  (default: ` `)
- `c`: Include a special character somewhere in the generated passphrase.  (default: `False`)

### FAQ

**Why can't I generate smaller passphrases?**

According to their [FAQ][diceware-faq], a 4-word passphrase only provides *51.6 bits* of entropy, almost the same number of bits as an 8 random ASCII character password.
Five word passphrases also are not allowed because they are easily breakable by a powerful botnet.

If you're looking for true secure passphrases, consider using a length of 8 words or more. Using the `-c` option to include a special character at random adds about 10 bits of entropy.

All of this assumes, of course, that your passphrase is kept secret.


[diceware]: http://world.std.com/~reinhold/diceware.html
[diceware-faq]: http://world.std.com/~reinhold/dicewarefaq.html
