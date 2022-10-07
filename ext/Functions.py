import sqlite3

import nextcord
from nextcord.ext import commands

CURR_DB = sqlite3.connect('curr.sqlite')
cursor = CURR_DB.cursor()


class EconomyFunc:
    def __init__(self, client: commands.Bot):
        self.client = client

    # region REMOVE_FUNCTIONS

    @staticmethod
    def rem_wallet(member: nextcord.Member, amount: int):
        wallet = EconomyFunc.check_wallet(member)
        cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, member.id))

    @staticmethod
    def rem_bank(member: nextcord.Member, amount: int):
        bank = EconomyFunc.check_bank(member)
        cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank - amount, member.id))

    @staticmethod
    def rem_max(member: nextcord.Member, amount: int):
        max_bank = EconomyFunc.check_max(member)
        cursor.execute("UPDATE curr SET max_bank = ? WHERE user_id = ?", (max_bank - amount, member.id))

    # endregion

    # region ADD_FUNCTIONS

    @staticmethod
    def add_wallet(member: nextcord.Member, amount: int):
        wallet = EconomyFunc.check_wallet(member)
        cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + amount, member.id))

    @staticmethod
    def add_bank(member: nextcord.Member, amount: int):
        bank = EconomyFunc.check_bank(member)
        cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank + amount, member.id))

    @staticmethod
    def add_max(member: nextcord.Member, amount: int):
        max_bank = EconomyFunc.check_max(member)
        cursor.execute("UPDATE curr SET max_bank = ? WHERE user_id = ?", (max_bank + amount, member.id))

    # endregion

    # region CHECK_FUNCTIONS

    @staticmethod
    def check_wallet(member: nextcord.Member, set0: bool = True):
        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {member.id} ")
        wallet = cursor.fetchone()

        if set0:
            # noinspection PyBroadException
            try:
                wallet = wallet[0]
            except:
                wallet = 0
        else:
            # noinspection PyBroadException
            try:
                wallet = wallet[0]
            except:
                wallet = wallet

        return wallet

    @staticmethod
    def check_bank(member: nextcord.Member, set0: bool = True):
        cursor.execute(f"SELECT bank FROM curr WHERE user_id = {member.id} ")
        bank = cursor.fetchone()

        if set0:
            # noinspection PyBroadException
            try:
                bank = bank[0]
            except:
                bank = 0
        else:
            # noinspection PyBroadException
            try:
                bank = bank[0]
            except:
                bank = bank

        return bank

    @staticmethod
    def check_max(member: nextcord.Member, set0: bool = True):
        cursor.execute(f"SELECT max_bank FROM curr WHERE user_id = {member.id} ")
        max_bank = cursor.fetchone()

        if set0:
            # noinspection PyBroadException
            try:
                max_bank = max_bank[0]
            except:
                max_bank = 0
        else:
            # noinspection PyBroadException
            try:
                max_bank = max_bank[0]
            except:
                max_bank = max_bank

        return max_bank

    # endregion


class MarketFunc:
    def __init__(self, client: commands.Bot):
        self.client = client

    # region REMOVE_FUNCTIONS

    @staticmethod
    def rem_item(column: str, member: nextcord.Member, amount: int):
        item = MarketFunc.check_item(column, member)
        cursor.execute(f"UPDATE inv SET {column} = ? WHERE user_id = ?", (item - amount, member.id))

    # endregion

    # region ADD_FUNCTIONS

    @staticmethod
    def add_item(column: str, member: nextcord.Member, amount: int):
        item = MarketFunc.check_item(column, member)
        cursor.execute(f"UPDATE inv SET {column} = ? WHERE user_id = ?", (item + amount, member.id))

    # endregion

    # region CHECK_FUNCTIONS

    @staticmethod
    def check_all_inv(member: nextcord.Member):
        cursor.execute(f"SELECT * FROM inv WHERE user_id = {member.id}")
        item = cursor.fetchone()

        return item

    @staticmethod
    def check_item(column: str, member: nextcord.Member, set0: bool = True):
        cursor.execute(f"SELECT {column} FROM inv WHERE user_id = {member.id}")
        item = cursor.fetchone()

        if set0:
            # noinspection PyBroadException
            try:
                item = item[0]
            except:
                item = 0
        else:
            # noinspection PyBroadException
            try:
                item = item[0]
            except:
                item = item

        return item

    # endregion
