import discord
import random
from darkmemer import life
from players import playerData

class pet:

    def __init__(self, pid, name, pdsc, nick = None):
        self.playerName = name
        self.player = life(pid, name, nick, pdsc)
        self.profile = bring_player.person.profile()
        self.wallet = bring_player.person.playerWallet()
        self.hasPet = True if profile[7] else False
        
    def petProfile(self, playerImageUrl):
        if self.hasPet:
            # description_ = self.profile[7][0] + self.profile[1]
            embed_ = discord.Embed(
                title = '{pName}\'s Pet ({petname})'.format(
                    pname = self.playerName,
                    petname = self.petProfile()[0]
                ),
                description = '',
                colour = discord.Colour.purple()
            )
            embed_.set_thumbnail(playerImageUrl)
        return embed_
    
    def namePet(self, newName):
        res = False
        if self.hasPet:
            self.petProfile()[0] = newName
            res = True
        return res
    
    def feedThePet(self):
        res = False
        if self.wallet > 0:
            self.player.person.spend(random.randint(10, 200))
            return res
        return res
    
    def patPet(self):
        return True
    
    def cleanPet(self):
        res = False
        if self.wallet > 0:
            self.player.person.spend(random.randint(30, 200))
            return res
        return res
    
    def playWithPet(self):
        return True