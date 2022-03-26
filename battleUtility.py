from sqlUtility import SqlUtil
from random import randint
from inventoryUtility import InvUtil
import sys


class BatUtil:

    # can be battle
    @staticmethod
    def stage_danger(conn, stage_flag):
        print("You are... in danger")
        if stage_flag == "no":
            enemy_color = BatUtil.pick_enemy_level()
            sql = "SELECT * FROM enemy WHERE type = '{}' ORDER BY RANDOM() LIMIT 1".format(enemy_color)
            enemy_d = SqlUtil.select_rows(conn, sql)
        elif stage_flag == "boss":
            sql = "SELECT * FROM enemy WHERE type = 'boss' ORDER BY RANDOM() LIMIT 1"
            enemy_d = SqlUtil.select_rows(conn, sql)
        elif stage_flag == "nega":
            sql = "SELECT * FROM player"
            nega_d = SqlUtil.select_rows(conn, sql)
            for d in nega_d:
                name = "nega " + d["name"]
                health = d["max_health"] * 2
                defense = d["defense"] * 2
                damage = d["damage"] * 2
                dodge = d["dodge"] * 2

            enemy_d = [{"name": name, "type": "nega", "health": health, "defense": defense,
                        "damage": damage, "dodge": dodge, "experience": 0}]

        sql = "SELECT * FROM player"
        player_d = SqlUtil.select_rows(conn, sql)
        equ_d = BatUtil.get_equipment(conn, player_d)
        BatUtil.do_battle(conn, enemy_d, player_d, equ_d)


    @staticmethod
    def pick_enemy_level():
        mon_number = randint(1,10)
        if mon_number < 6:
            enemy_color = "red"
        elif mon_number > 8:
            enemy_color = "black"
        else:
            enemy_color = "blue"
        return enemy_color


    @staticmethod
    def get_equipment(conn, player_d):
        for d in player_d:
            helm = d["helm_id"]
            chest = d["chest_id"]
            pants = d["pants_id"]
            boots = d["boots_id"]
            weapon = d["weapon_id"]

        sql = "SELECT stat FROM bag WHERE bag_id = {}".format(helm)
        defense = 0
        temp_d = SqlUtil.select_rows(conn, sql)
        for t in temp_d:
            temp = t["stat"]
        defense = defense + temp
        sql = "SELECT stat FROM bag WHERE bag_id = {}".format(chest)
        temp_d = SqlUtil.select_rows(conn, sql)
        for t in temp_d:
            temp = t["stat"]
        defense = defense + temp

        sql = "SELECT stat FROM bag WHERE bag_id = {}".format(pants)
        dodge = 0
        temp_d = SqlUtil.select_rows(conn, sql)
        for t in temp_d:
            temp = t["stat"]
        dodge = dodge + temp
        sql = "SELECT stat FROM bag WHERE bag_id = {}".format(boots)
        temp_d = SqlUtil.select_rows(conn, sql)
        for t in temp_d:
            temp = t["stat"]
        dodge = dodge + temp

        sql = "SELECT stat FROM bag WHERE bag_id = {}".format(weapon)
        damage = 0
        temp_d = SqlUtil.select_rows(conn, sql)
        for t in temp_d:
            temp = t["stat"]
        damage = damage + temp

        equipment = [{"defense": defense, "dodge": dodge, "damage": damage}]
        return equipment

    @staticmethod
    def do_battle(conn, enemy_d, player_d, equ_d):
        for d in enemy_d:
            # name, type, health, defense, damage, dodge, experience
            e_name = d["name"]
            e_hp = d["health"]
            e_def = d["defense"]
            e_dmg = d["damage"]
            e_dog = d["dodge"]
            e_exp = d["experience"]

        for d in player_d:
            # current_health, max_health, defense, damage, dodge, level
            p_cur_hp = d["current_health"]
            p_max_hp = d["max_health"]
            p_def = d["defense"]
            p_dmg = d["damage"]
            p_dog = d["dodge"]
            p_stage = d["game_stage"]
            p_lvl = d["level"]

        for d in equ_d:
            # defense, dodge, damage
            equ_def = d["defense"]
            equ_dog = d["dodge"]
            equ_dmg = d["damage"]

        temp_e_def = 0
        temp_p_def = 0
        print("You encountered a ", e_name)
        while e_hp > 0 and p_cur_hp > 0:
            print("Player Hp: ", p_cur_hp, "/", p_max_hp, "  Enemy Hp: ", e_hp)
            user_input = ""
            while user_input != "attack" and user_input != "defend" and user_input != "use":
                print("Do you want to attack, defend or use potion? Type attack, defend or use")
                user_input = input()
                if user_input == "attack":
                    total_p_dmg = (p_dmg * p_lvl) + equ_dmg
                    total_e_def = e_def + temp_e_def
                    damage = BatUtil.calculate_damage(total_p_dmg, total_e_def, e_dog)
                    print("You did ", damage, " damage!!")
                    e_hp = e_hp - damage
                    temp_e_def = 0
                elif user_input == "defend":
                    print("You defended")
                    temp_p_def = p_def / 2
                elif user_input == "use":
                    InvUtil.inventory_use(conn)
                    sql = "SELECT * FROM player"
                    temp_d = SqlUtil.select_rows(conn, sql)
                    for d in temp_d:
                        p_cur_hp = d["current_health"]

            # enemy attacks or defends
            if randint(0, 10) > 3:
                total_p_def = p_def + temp_p_def + equ_def
                total_p_dog = p_dog + equ_dog
                damage = BatUtil.calculate_damage(e_dmg, total_p_def, total_p_dog)
                print("Enemy did ", damage, " damage!!")
                p_cur_hp = p_cur_hp - damage
                temp_p_def = 0
            else:
                print("Enemy defended")
                temp_e_def = e_def / 2

            # have to refresh health in database because of bad coding...
            sql = "UPDATE player SET current_health = {}".format(p_cur_hp)
            SqlUtil.update_rows(conn, sql)

        if e_hp > 0:
            sys.exit("you died")
        else:
            print("You won and found something")
            BatUtil.update_player(conn, e_exp)
            BatUtil.get_item(conn)


    @staticmethod
    def calculate_damage(x_dmg, x_def, x_dog):
        print("in calc damage")
        damage = 0
        if randint(0, 10) > (x_dog * 10):
            damage = x_dmg - x_def

        if damage < 0:
            damage = 0

        return damage


    @staticmethod
    def update_player(conn, exp_new):
        sql = "SELECT * FROM player"
        player_d = SqlUtil.select_rows(conn, sql)
        for d in player_d:
            stage = d["game_stage"]
            exp_total = d["total_experience"]
            exp_left = d["next_level_experience"]
            lvl = d["level"]

        stage = stage + 1
        exp_total = exp_total + exp_new
        if exp_left < exp_new:
            lvl = lvl + 1
            exp_over = exp_new - exp_left
            exp_left = (lvl * 100) - exp_over
        else:
            exp_left = exp_left - exp_new

        sql = "UPDATE player SET total_experience = {}, level = {},  next_level_experience = {}, game_stage = {}"\
            .format(exp_total, lvl, exp_left, stage)
        SqlUtil.update_rows(conn, sql)


    @staticmethod
    def get_item(conn):
        chance = randint(1, 100)
        sql = "SELECT * FROM items WHERE rarity < {} ORDER BY RANDOM() LIMIT 1".format(chance)
        item_d = SqlUtil.select_rows(conn, sql)
        print("You got a ", item_d)
        for d in item_d:
            name = d["name"]
            typeroonie = d["type"]
            stat_type = d["stat_type"]
            stat = d["stat"]

        sql = "INSERT INTO bag (name, type, stat_type, stat) VALUES (?,?,?,?)"
        value = (name, typeroonie, stat_type, stat)
        SqlUtil.insert_rows(conn, sql, value)

    # can be battle, loot, or damage
    @staticmethod
    def stage_loot(conn):
        sql = "SELECT game_stage, current_health FROM player"
        stage_d = SqlUtil.select_rows(conn, sql)
        for d in stage_d:
            stage = d["game_stage"]
            hp = d["current_health"]

        chance = randint(1, 3)
        if chance == 1:
            BatUtil.stage_danger(conn, "no")
        elif chance == 2:
            # get damage
            damage = (stage * 5) + 10
            print("You fell into a trap, idiot. You took ", damage, " damage!")
            hp = hp - damage
            stage = stage + 1
            sql = "UPDATE player SET current_health = {}, game_stage = {}" \
                .format(hp, stage)
            SqlUtil.update_rows(conn, sql)
        elif chance == 3:
            # get loot
            print("You found something...")
            new_exp = stage * 5
            BatUtil.update_player(conn, new_exp)
            BatUtil.get_item(conn)


