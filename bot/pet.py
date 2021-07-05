import discord
import random
from darkmemer import player
from playerData import playerData

class pet:

    def __init__(self, pid, name, pdsc):
        self.playerName = name
        self.player = player(pid, name, pdsc)
        self.profile = self.player.profile()
        self.wallet = self.player.playerWallet()
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
        if self.hasPet:
            self.petProfile()[0] = newName
            return True
        return False
    
    def feedThePet(self):
        if self.wallet > 0:
            self.player.spend(random.randint(10, 200))
            return True
        return False
    
    def patPet(self):
        return True
    
    def cleanPet(self):
        if self.wallet > 0:
            self.player.spend(random.randint(30, 200))
            return True
        return False
    
    def playWithPet(self):
        return True