# ----- data file content format ----- #
# URL:                                 #
#                                      #
# Date: dd-mm-yyyy                     #
# Time: hh-mm-ss                       #
# Cursor level:                        #
# Grandma level:                       #
# Factory level:                       #
# Mine level:                          #
# Shipment level:                      #
# Alchemy lab level:                   #
# Portal level:                        #
# Time machine level:                  #
# Save key:                            #
# ------------------------------------ #

import datetime

FILE_PATH = "data.txt"


class DataManager:
    @staticmethod
    def load_game() -> str:
        try:
            with open(file=FILE_PATH, mode="r") as file:
                old_content = file.readlines()
        except FileNotFoundError:
            print("No previous game saves found.")
            return None
        else:
            save_key = old_content[-1].split()[-1]
            return save_key

    @staticmethod
    def save_game(is_new_game: bool, game_url: str, game_data: tuple, save_key: str):
        # --- unpack game data --- #
        (cps, money, upgrade_amounts, upgrade_prices) = game_data
        [cursor_amount, grandma_amount, factory_amount, mine_amount, shipment_amount, alchemy_lab_amount, portal_amount, time_machine_amount] = upgrade_amounts
        # --- write new content --- #
        date_time = datetime.datetime.now()
        new_content = f"\n\nDate: {date_time.day:02d}-{date_time.month:02d}-{date_time.year:04d}\nTime: {date_time.hour:02d}:{date_time.minute:02d}:{date_time.second:02d}\nCPS: {cps}\nMoney: {money}\nCursor level: {cursor_amount}\nGrandma level: {grandma_amount}\nFactory level: {factory_amount}\nMine level: {mine_amount}\nShipment level: {shipment_amount}\nAlchemy lab level: {alchemy_lab_amount}\nPortal level: {portal_amount}\nTime machine level: {time_machine_amount}\nSave key: {save_key}"
        if is_new_game:
            new_file_head = f"URL: {game_url}"
            first_content = new_file_head + new_content
            with open(file=FILE_PATH, mode="w") as file:
                file.write(first_content)
        else:
            with open(file=FILE_PATH, mode="a") as file:
                file.write(new_content)
        print("Game saved.")
