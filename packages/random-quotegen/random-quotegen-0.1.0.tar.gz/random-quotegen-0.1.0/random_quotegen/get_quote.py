import random

from random_quotegen.quotes import quotes


def get_quote():
    """
    Get a random quote.

    Get randomly selected quote from the database of quotes.

    :return: selected quote
    :rtype: dict
    """
    return quotes[random.randint(0, len(quotes) - 1)]
