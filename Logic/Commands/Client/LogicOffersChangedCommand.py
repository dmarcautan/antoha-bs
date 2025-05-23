from Logic.Shop import Shop
from Utils.Writer import Writer
import json

class LogicOffersChangedCommand(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.player = player
        self.id = 24111


    def encode(self):
        self.writeVint(211)
        Shop.loadOffers(self)
        wow = self.offers
        count = len(wow)
        self.writeVint(count)
        for i in range(count):
            item = wow[i]
            if item['ID'][0] != 0 and item['ID'][1] != 0 and item['ID'][2] != 0:
                self.writeVint(3)
                self.writeVint(item['ID'][0]) # ItemID
                self.writeVint(item['Multiplier'][0]) # Ammount
                self.writeScId(16, item['BrawlerID'][0])
                self.writeVint(item['SkinID'][0]) # ItemID
                self.writeVint(item['ID'][1]) # ItemID
                self.writeVint(item['Multiplier'][1]) # Ammount
                self.writeScId(16, item['BrawlerID'][1])
                self.writeVint(item['SkinID'][1]) # ItemID
                self.writeVint(item['ID'][2]) # ItemID
                self.writeVint(item['Multiplier'][2]) # Ammount
                self.writeScId(16, item['BrawlerID'][2])
                self.writeVint(item['SkinID'][2]) # ItemID

            elif item['ID'][0] != 0 and item['ID'][1] != 0:
                self.writeVint(2)
                self.writeVint(item['ID'][0]) # ItemID
                self.writeVint(item['Multiplier'][0]) # Ammount
                self.writeScId(16, item['BrawlerID'][0])
                self.writeVint(item['SkinID'][0]) # ItemID
                self.writeVint(item['ID'][1]) # ItemID
                self.writeVint(item['Multiplier'][1]) # Ammount
                self.writeScId(16, item['BrawlerID'][1])
                self.writeVint(item['SkinID'][1]) # ItemID

            else:
                if self.player.UnlockedBrawlers[f"{int(item['BrawlerID'][0])}"] == 1:
                    self.writeVint(1)
                    self.writeVint(item['ID'][0])
                    self.writeVint(item['Multiplier'][0])
                    self.writeScId(16, item['BrawlerID'][0])
                    self.writeVint(item['SkinID'][0])
                else:
                    self.writeVint(1)
                    self.writeVint(1) # ItemID
                    self.writeVint(0) # Ammount
                    self.writeScId(16, 0)
                    self.writeVint(0) # ItemID
                    
            self.writeVint(item['ShopType'])  # [0 = Offer, 2 = Skins 3 = Star Shop]

            self.writeVint(item['Cost'])  # Cost
            self.writeVint(item['Timer'])

            self.writeVint(item['OfferView']) # Offer View | 0 = Absolutely "NEW", 1 = "NEW", 2 = Viewed
            self.writeVint(100)
            if self.player.low_id in item["WhoBuyed"]:
                self.writeBoolean(True)
            else:
                if self.player.UnlockedBrawlers[f"{int(item['BrawlerID'][0])}"] == 0:
                    self.writeBoolean(True)
                else:
                    self.writeBoolean(False)
        
            self.writeBoolean(False)
            if self.player.UnlockedBrawlers[f"{int(item['BrawlerID'][0])}"] == 0:
                self.writeVint(0)
            else:
                self.writeVint(item['ShopDisplay'])# [0 = Normal, 1 = Daily Deals]
            self.writeVint(item['OldCost'])#oldCost
            self.writeVint(0)

            self.writeInt(0)
            self.write_string_reference(item['OfferTitle'])
            self.writeBoolean(False)
            self.writeString(item['OfferBGR'])
            self.writeVint(0)
            self.writeBoolean(False)
            self.writeVint(item['ETType']) # Extra Text Type | 1 = Factor(?x),
            self.writeVint(item['ETMultiplier']) # Extra Text

    def process(self):
        self.offers=[]
        with open("JSON/offers.json", "r",encoding='utf-8') as f:
            data = json.load(f)
            for i in data.values():
                self.offers.append(i)
        with open("JSON/offers.json", "r",encoding='utf-8') as f:
            data = json.load(f)
        data[str(i)]["WhoBuyed"].append(int(self.player.low_id))
        with open("JSON/offers.json", "w",encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)