from sqlUtility import SqlUtil


class InvUtil:

    @staticmethod
    def inventory_main(conn):
        print("in inventory main")
        sql = "SELECT * FROM bag"
        inv_d = SqlUtil.select_rows(conn, sql)
        print("name, type, stat type, stat", )
        for d in inv_d:
            inv_name = d["name"]
            inv_type = d["type"]
            inv_stat_type = d["stat_type"]
            inv_stat = d["stat"]
            print(inv_name, ",", inv_type, ",", inv_stat_type, ",", inv_stat)

        user_input = ""
        while user_input != "no":
            print("Would you like to use a potion or swap an item? Type use, swap or no")
            user_input = input()
            if user_input == "use":
                InvUtil.inventory_use(conn)
            elif user_input == "swap":
                InvUtil.inventory_swap(conn)


    @staticmethod
    def inventory_use(conn):
        sql = "SELECT * FROM bag WHERE type = 'heal'"
        inv_d = SqlUtil.select_rows(conn, sql)
        print("id, name, type, stat type, stat")
        inv_id_arr = []
        for d in inv_d:
            inv_id = d["bag_id"]
            inv_id_arr.append(inv_id)
            inv_name = d["name"]
            inv_type = d["type"]
            inv_stat_type = d["stat_type"]
            inv_stat = d["stat"]
            print(inv_id, ",", inv_name, ",", inv_type, ",", inv_stat_type, ",", inv_stat)

        print("Which item would you like to use?")
        user_input = int(input())
        if user_input in inv_id_arr:
            print("good choice")
            InvUtil.use_potion(conn, user_input, inv_d)
        else:
            print("you dumb")


    @staticmethod
    def use_potion(conn, user_input, inv_d):
        for d in inv_d:
            if d["bag_id"] == user_input:
                inv_stat = d["stat"]

        sql = "SELECT current_health, max_health FROM player"
        player_d = SqlUtil.select_rows(conn, sql)
        for di in player_d:
            cur_health = di["current_health"]
            max_health = di["max_health"]

        cur_health = cur_health + inv_stat

        if cur_health > max_health:
            sql = "UPDATE player SET current_health = {}".format(max_health)
        else:
            sql = "UPDATE player SET current_health = {}".format(cur_health)
        SqlUtil.select_rows(conn, sql)

        sql = "DELETE FROM bag WHERE bag_id = {}".format(user_input)
        SqlUtil.select_rows(conn, sql)


    @staticmethod
    def inventory_swap(conn):
        sql = "SELECT * FROM bag WHERE type <> 'heal'"
        inv_d = SqlUtil.select_rows(conn, sql)
        print("id, name, type, stat type, stat")
        inv_id_arr = []
        for d in inv_d:
            inv_id = d["bag_id"]
            inv_id_arr.append(inv_id)
            inv_name = d["name"]
            inv_type = d["type"]
            inv_stat_type = d["stat_type"]
            inv_stat = d["stat"]
            print(inv_id, ",", inv_name, ",", inv_type, ",", inv_stat_type, ",", inv_stat)

        print("Which item would you like to swap?")
        user_input = int(input())
        if user_input in inv_id_arr:
            print("good choice")
            InvUtil.swap_item(conn, user_input, inv_d)
        else:
            print("you dumb")


    @staticmethod
    def swap_item(conn, user_input, inv_d):
        for d in inv_d:
            if d["bag_id"] == user_input:
                inv_type = d["type"]

        if inv_type == "helm":
            sql = "UPDATE player SET helm_id = {}".format(user_input)
        elif inv_type == "chest":
            sql = "UPDATE player SET chest_id = {}".format(user_input)
        elif inv_type == "pants":
            sql = "UPDATE player SET pants_id = {}".format(user_input)
        elif inv_type == "boots":
            sql = "UPDATE player SET boots_id = {}".format(user_input)
        elif inv_type == "weapon":
            sql = "UPDATE player SET weapon_id = {}".format(user_input)

        SqlUtil.select_rows(conn, sql)
