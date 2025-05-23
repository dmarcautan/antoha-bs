import json, random
from database.DataBase import database
import sqlite3
class Quest:
    def EncodeQuest(self):
        self.writeBoolean(True) # Quests Boolean
        conn = sqlite3.connect('database/Player/plr.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plrs WHERE lowID=?', (self.player.low_id,))
        user = cursor.fetchone()
        self.player.quests = json.loads(user_data[29])
        questsCount = 0
        for i in quests:
            if i["state"] == 0:
                questsCount += 15
        
        if questsCount > 0:
            for item in quests:
                self.writeVint(questsCount)
                self.writeVint(0)
                self.writeVint(0)
                self.writeVint(1) # Mission Type
                self.writeVint(item['0']) # Current Quest Goal
                self.writeVint(item['8']) # Max Quest Goal
                self.writeVint(item['1000']) # Tokens Reward
                self.writeVint(0)
                self.writeVint(0) # Current Level 
                self.writeVint(0) # Max Level
                self.writeVint(item['QT']) # Quest Type | 0 = Season Quest, 1 = Daily Quest
                self.writeBoolean(False) # Brawl Pass Exclusive
                self.writeScId(16, item['id']) # Brawler ID
                self.writeVint(item['GM']) # Gamemode ID
                self.writeVint(0)
        elif questsCount == 0:
            self.writeVint(0)