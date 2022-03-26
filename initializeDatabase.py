from sqlite3 import Error
from sqlUtility import SqlUtil


def sql_table(conn, table_sql):
    try:
        c = conn.cursor()
        c.execute(table_sql)
    except Error as e:
        print(e)


def create_tables(conn):
    sql_create_player_table = """ CREATE TABLE IF NOT EXISTS player (
                                        name text PRIMARY KEY,
                                        class text,
                                        current_health integer,
                                        max_health integer,
                                        defense integer,
                                        damage integer,
                                        dodge float,
                                        helm_id integer,
                                        chest_id integer,
                                        pants_id integer,
                                        boots_id integer,
                                        weapon_id integer,
                                        total_experience integer,
                                        level integer,
                                        next_level_experience integer,
                                        game_stage integer
                                    ); """
    sql_drop_player_table = 'DROP TABLE IF EXISTS player'

    sql_create_active_enemy_table = """CREATE TABLE IF NOT EXISTS active_enemy (
                                    name text PRIMARY KEY,
                                    health integer,
                                    defense integer,
                                    damage integer,
                                    dodge float
                                );"""

    sql_drop_active_enemy_table = 'DROP TABLE IF EXISTS active_enemy'

    sql_create_bag_table = """CREATE TABLE IF NOT EXISTS bag (
                                    bag_id integer PRIMARY KEY,
                                    name text,
                                    type text,
                                    stat_type text,
                                    stat integer
                                );"""

    sql_drop_bag_table = 'DROP TABLE IF EXISTS bag'

    sql_create_enemy_table = """CREATE TABLE IF NOT EXISTS enemy (
                                    name text PRIMARY KEY,
                                    type text,
                                    health integer,
                                    defense integer,
                                    damage integer,
                                    dodge float,
                                    experience integer
                                );"""

    sql_drop_enemy_table = 'DROP TABLE IF EXISTS enemy'

    sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                                    name text PRIMARY KEY,
                                    rarity integer,
                                    type text,
                                    stat_type text,
                                    stat integer
                                );"""

    sql_drop_items_table = 'DROP TABLE IF EXISTS items'

    # create tables
    if conn is not None:
        sql_table(conn, sql_drop_player_table)
        sql_table(conn, sql_create_player_table)
        sql_table(conn, sql_drop_active_enemy_table)
        sql_table(conn, sql_create_active_enemy_table)
        sql_table(conn, sql_drop_bag_table)
        sql_table(conn, sql_create_bag_table)
        sql_table(conn, sql_drop_enemy_table)
        sql_table(conn, sql_create_enemy_table)
        sql_table(conn, sql_drop_items_table)
        sql_table(conn, sql_create_items_table)

        conn.commit
        display_tables(conn)
    else:
        print("Error! cannot create the database connection.")


def display_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())


def create_items(conn):
    items_sql = "INSERT INTO items (name, rarity, type, stat_type, stat) " \
                "VALUES (?,?,?,?,?)"
    items_values = ("potion", 0, "heal", "hp", 50)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("super potion", 50, "heal", "hp", 100)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("rusty hat", 10, "helm", "defense", 10)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("rusty vest", 10, "chest", "defense", 8)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("rusty pants", 10, "pants", "dodge", 4)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("rusty bootz", 10, "boots", "dodge", 4)
    SqlUtil.insert_rows(conn, items_sql, items_values)
    items_values = ("death sword", 25, "weapon", "damage", 15)
    SqlUtil.insert_rows(conn, items_sql, items_values)


def create_bag(conn):
    bag_sql = "INSERT INTO bag (bag_id, name, type, stat_type, stat) " \
                "VALUES (?,?,?,?,?)"
    bag_values = (1, "potion", "heal", "hp", 50)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (2, "smelly hat", "helm", "defense", 8)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (3, "smelly vest", "chest", "defense", 6)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (4, "smelly pants", "pants", "dodge", 4)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (5, "smelly bootz", "boots", "dodge", 2)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (6, "schword", "weapon", "damage", 10)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (7, "potion", "heal", "hp", 50)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)
    bag_values = (8, "schwordier", "weapon", "damage", 50)
    SqlUtil.insert_rows(conn, bag_sql, bag_values)


def create_enemy(conn):
    enemy_sql = "INSERT INTO enemy (name, type, health, defense, damage, dodge, experience) " \
                "VALUES (?,?,?,?,?,?,?)"
    enemy_values = ("red fox", "red", 30, 10, 25, .2, 50)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)
    enemy_values = ("red xof", "red", 30, 10, 25, .2, 50)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)
    enemy_values = ("blue fox", "blue", 60, 15, 35, .2, 75)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)
    enemy_values = ("blue xof", "blue", 60, 15, 35, .2, 75)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)
    enemy_values = ("black fox", "black", 80, 20, 45, .2, 100)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)
    enemy_values = ("Kanye West", "boss", 150, 50, 50, .2, 200)
    SqlUtil.insert_rows(conn, enemy_sql, enemy_values)


def create_data(conn):
    player_sql = "INSERT INTO player (name, class, current_health, max_health, defense, damage, dodge, " \
                 "helm_id, chest_id, pants_id, boots_id, weapon_id, total_experience, level, next_level_experience, " \
                 "game_stage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    player_values = ("Dead", "Elf", 100, 150, 10, 20, .1, 2, 3, 4, 5, 6, 0, 1, 100, 1)
    SqlUtil.insert_rows(conn, player_sql, player_values)
    print(SqlUtil.select_rows(conn, "SELECT * FROM player"))

    create_bag(conn)
    print(SqlUtil.select_rows(conn, "SELECT * FROM bag"))

    create_items(conn)
    print(SqlUtil.select_rows(conn, "SELECT * FROM items"))

    create_enemy(conn)
    print(SqlUtil.select_rows(conn, "SELECT * FROM enemy"))


def main():
    conn = SqlUtil.create_connection()
    create_tables(conn)
    create_data(conn)
    conn.commit()


if __name__ == '__main__':
    main()
