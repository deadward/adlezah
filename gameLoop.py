from sqlUtility import SqlUtil
from inventoryUtility import InvUtil
from battleUtility import BatUtil


def stage_start(stage, conn):
    # player can take potion or switch gear
    user_input = ""
    while user_input != "no":
        print("Would you like to check your inventory? Type yes or no")
        user_input = input()
        if user_input == "yes":
            InvUtil.inventory_main(conn)

    # play does stage action
    if stage == 5 or stage == 10:
        # boss fight
        print("boss fight")
        stage_loop(conn, "boss")
    elif stage == 11:
        # nega boss fight
        print("nega boss fight")
        stage_loop(conn, "nega")
    else:
        # user choice
        print("stage not boss")
        stage_loop(conn, "no")


def stage_loop(conn, stage_flag):
    if stage_flag == "no":
        user_input = ""
        while user_input != "danger" and user_input != "loot":
            print("Search for danger or look for Loot? Type danger or loot")
            user_input = input()
            if user_input == "danger":
                BatUtil.stage_danger(conn, "no")
            elif user_input == "loot":
                BatUtil.stage_loot(conn)
    elif stage_flag == "boss":
        BatUtil.stage_danger(conn, "boss")
    elif stage_flag == "nega":
        BatUtil.stage_danger(conn, "nega")

def main():
    conn = SqlUtil.create_connection()
    # get player health and game progress
    player_health = 1
    player_game_stage = 0
    while player_health > 0 and player_game_stage < 12:
        # only ever one record in the player table right now
        player_d = SqlUtil.select_rows(conn, "SELECT current_health, game_stage, level FROM player")
        for d in player_d:
            player_health = d["current_health"]
            player_game_stage = d["game_stage"]
            player_level = d["level"]
        print("Current health: ", player_health)
        print("Current game stage: ", player_game_stage)
        print("Current level: ", player_level)
        stage_start(player_game_stage, conn)


if __name__ == '__main__':
    main()
