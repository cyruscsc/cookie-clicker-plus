import time
from data_manager import DataManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class AutoClicker:
    def __init__(self, driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))):
        """Initialize Auto-Clicker, open url, set clicking target."""
        self.url = "http://orteil.dashnet.org/experiments/cookie/"
        self.driver = driver
        self.driver.get(url=self.url)
        self.target = self.driver.find_element(By.ID, "cookie")
        self.save_key = DataManager.load_game()
        if self.save_key is None:
            self.is_new_game = True
        else:
            self.is_new_game = False
            self.import_save(save_key=self.save_key)

    def auto_click(self, stop_after_min: int, break_after_sec: int):
        """Recursion: Click the target automatically, buy upgrade after certain seconds."""
        time_stop = time.time() + stop_after_min * 60
        while time.time() < time_stop:
            time_break = time.time() + break_after_sec
            while time.time() < time_break:
                self.target.click()
            self.buy_upgrade(game_data=self.get_data())
        game_data = self.get_data()
        DataManager.save_game(is_new_game=self.is_new_game, game_url=self.url, game_data=game_data, save_key=self.generate_save_key(game_data=game_data))
        self.driver.quit()

    def buy_upgrade(self, game_data: tuple):
        """Buy the most powerful upgrade available."""
        # --- unpack game data --- #
        (cps, money, upgrade_amounts, upgrade_prices) = game_data
        [cursor_price, grandma_price, factory_price, mine_price, shipment_price, alchemy_lab_price, portal_price, time_machine_price] = upgrade_prices
        # --- get and unpack upgrade buttons --- #
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "#store div b")
        [cursor_button, grandma_button, factory_button, mine_button, shipment_button, alchemy_lab_button, portal_button, time_machine_button, elder_pledge_button] = buttons
        buttons.remove(elder_pledge_button)
        # --- check and buy upgrade --- #
        if money >= time_machine_price:
            time_machine_button.click()
        elif money >= portal_price:
            portal_button.click()
        elif money >= alchemy_lab_price:
            alchemy_lab_button.click()
        elif money >= shipment_price:
            shipment_button.click()
        elif money >= mine_price:
            mine_button.click()
        elif money >= factory_price:
            factory_button.click()
        elif money >= grandma_price:
            grandma_button.click()
        elif money >= cursor_price:
            cursor_button.click()
        else:
            pass

    def get_data(self) -> tuple[int, int, list, list]:
        """Get all game data."""
        cps = float(self.driver.find_element(By.ID, "cps").text.split()[-1])
        money = int(self.driver.find_element(By.ID, "money").text.replace(",", ""))
        upgrade_amounts = [int(amount_element.text) for amount_element in self.driver.find_elements(By.CLASS_NAME, "amount")]
        while len(upgrade_amounts) < 8:  # in case some upgrades are not bought yet,
            upgrade_amounts.append(0)    # so there are no elements with class name "amount" for them
        price_elements = self.driver.find_elements(By.CSS_SELECTOR, "#store div b")  # there are 9 price_elements,
        price_elements.remove(price_elements[-1])                                    # but the last one is actually empty and unavailable
        upgrade_prices = []
        for price_element in price_elements:
            price_text_list = price_element.text.replace(",", "").split()
            upgrade_prices.append(int(price_text_list[-1]))
        return cps, money, upgrade_amounts, upgrade_prices

    def generate_save_key(self, game_data: tuple) -> str:
        # --- unpack and organize game data --- #
        (cps, money, upgrade_amounts, upgrade_prices) = game_data
        upgrade_amounts_prices = []
        for n in range(len(upgrade_prices)):
            upgrade_amounts_prices.append(str(upgrade_amounts[n]))
            upgrade_amounts_prices.append(str(upgrade_prices[n]))
        # --- generate save key --- #
        self.save_key = f"{cps}|{money}|" + "|".join(upgrade_amounts_prices)
        return self.save_key

    def import_save(self, save_key: str):
        import_save_button = self.driver.find_element(By.ID, "importSave")
        import_save_button.click()
        alert = self.driver.switch_to.alert
        alert.send_keys(f"{save_key}")
        alert.accept()
