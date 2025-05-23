from Server.Club.MyAllianceMessage import MyAllianceMessage
from Server.Club.AllianceStreamMessage import AllianceStreamMessage
from Server.Club.AllianceJoinOkMessage import AllianceJoinOkMessage
from Server.Club.JoinFail import AllianceJoinFail
from Server.Club.AllianceChatServer import AllianceChatServer
from Server.Login.LoginFailedMessage import LoginFailedMessage
from database.DataBase import DataBase
from Utils.Reader import BSMessageReader
import time

class JoinAllianceMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.player.club_high_id = self.read_int()
        self.player.club_low_id = self.read_int()

    def process(self):
        # Загрузка данных клуба
        DataBase.loadClub(self, self.player.club_low_id)
        
        # Проверка, не достигнуто ли максимальное количество участников
        if self.clubmembercount == 100:
            AllianceJoinFail(self.client, self.player).send()
            return

        # Проверка времени последнего выхода из клуба
        if hasattr(self.player, 'last_club_exit_time'):
            if (time.time() - self.player.last_club_exit_time) < 5:
                self.player.err_code = 1
                LoginFailedMessage(self.client, self.player, "Так нельзя делать!").send()
                return  # добавляем return, чтобы не продолжать выполнение

        # Установка роли и ID клуба для игрока
        self.player.club_role = 1
        DataBase.replaceValue(self, 'clubRole', 1)
        DataBase.replaceValue(self, 'clubID', self.player.club_low_id)

        # Добавление игрока в клуб и запись сообщения
        DataBase.AddMember(self, self.player.club_low_id, self.player.low_id, self.player.name, 1)
        DataBase.Addmsg(self, self.player.club_low_id, 4, 0, self.player.low_id, self.player.name, self.player.club_role, 3)

        # Отправка информации игроку
        AllianceJoinOkMessage(self.client, self.player).send()
        MyAllianceMessage(self.client, self.player, self.player.club_low_id).send()
        AllianceStreamMessage(self.client, self.player, self.player.club_low_id, 0).send()

        # Перезагрузка данных клуба после добавления нового участника
        DataBase.loadClub(self, self.player.club_low_id)