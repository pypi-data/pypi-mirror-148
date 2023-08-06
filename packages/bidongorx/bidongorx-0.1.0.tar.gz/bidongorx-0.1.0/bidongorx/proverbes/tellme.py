
import random

def proverbe():
    """ Retourne un proverbe d'Aqabah au hasard

    Returns:
        (str): proverbe
    """

    list_of_proverbes = ["Le goudron amer de la dignité vaut mieux que le miel de la tranquillité",
                        "Conseille l'ignorant, il te prendra pour son ennemi",
                        "Chose donnée de bon coeur vaut son pesant d'or",
                        "N'ouvre la bouche que si tu es sûr que ce que tu vas dire est plus beau que le silence",
                        "Qui vous connait petit ne vous respecte pas grand",
                        "Qui mange seul s’étrangle seul",]
    
    return random.choice(list_of_proverbes)