from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import datetime

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_room(room, room_hoster):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 调用datetime方法获取当前时间
    with open("get_roomdata.txt", "a", encoding="utf-8") as file:
        file.write(f"{current_time}：检测到有房间，房间号：{room}---->房主:{room_hoster}\n")
    # 写入roomdata.txt文件，追加模式，utf-8编码

def get_room_ids(driver):
    rooms_info = []
    try:
        # 等待父容器出现
        card_items = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'QuickCardItem__Wrapper-sc-6tfrzy-0')]"))
        )

        for card_item in card_items:
            try:
                # 查找房间码
                room_id_div = card_item.find_element(By.XPATH, ".//div[contains(@class, 'QuickCardItem__CardRoomIdText') and contains(text(), '房间码')]")
                room_id_text = room_id_div.text.strip().replace("房间码：", "")
                logger.info(f"房间码: {room_id_text}")

                # 查找房东名
                owner_name_div = card_item.find_element(By.XPATH, ".//div[contains(@class, 'QuickCardItem__RoleInfoDetailName')]")
                owner_name_text = owner_name_div.text.strip()
                logger.info(f"房主名: {owner_name_text}")
                
                rooms_info.append((room_id_text, owner_name_text))
            except Exception as e:
                logger.warning(f"在当前卡片中未找到所有所需元素: {e}")

    except Exception as e:
        logger.error(f"未找到目标元素: {e}")

    return rooms_info

if __name__ == "__main__":
    # 设置Edge选项
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    edge_options.add_argument("--proxy-server='direct://'")  # 禁用代理
    edge_options.add_argument("--proxy-bypass-list=*")
    edge_options.add_argument("--disable-cache")  # 禁用缓存

    # 设置EdgeDriver路径
    service = Service(r'E:\download\edgedriver_win64\msedgedriver.exe')  # 使用原始字符串或双反斜杠

    # 启动WebDriver
    driver = webdriver.Edge(service=service, options=edge_options)

    # 打开目标URL
    url = "https://game.skland.com/popucom/team-building-tools?header=0"
    driver.get(url)

    try:
        while True:
            rooms_info = get_room_ids(driver)
            for room_id, owner_name in rooms_info:
                save_room(room_id, owner_name)
            # 等待5秒后再次请求
            time.sleep(3)
    finally:
        # 关闭WebDriver
        driver.quit()



