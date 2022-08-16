from fastapi.testclient import TestClient

from ..models.stock import Stock
from ..main import app
from ..config import settings
import unittest
import time
from ..consumer import client as mqtt_client
from .test_user import test_deposit


client = TestClient(app)


class TestStock(unittest.TestCase):
    def setUp(self):
        self.client = mqtt_client
        self.broker = settings.MQTT_HOST
        self.port = 1883
        self.stock_id: str = ""
        test_deposit()

    def test_connection(self):  # test to check connection to broker
        connected = self.client.connect(self.broker, self.port)
        self.client.loop_start()
        time.sleep(3)
        self.stock_id = Stock.all()[0].id
        self.assertTrue(connected == 0)

    def test_stock(self):
        response = client.get("/stock/")
        self.assertTrue(response.status_code)

    def test_stock_retrieve(self):
        response = client.get(f"/stock/{self.stock_id}")
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_DAY(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "Day",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_DAY_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "Day",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_GTC(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTC",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_GTC_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTC",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_IOC(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "IOC",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_IOC_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "IOC",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_FOK(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "FOK",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_FOK_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "FOK",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_GTD(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTD",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Market_GTD_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTD",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_DAY(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "DAY",
                "all_or_none": True,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_DAY_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "DAY",
                "all_or_none": False,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_GTC(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTC",
                "all_or_none": True,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_GTC_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTC",
                "all_or_none": False,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_IOC(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "IOC",
                "all_or_none": True,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_IOC_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "IOC",
                "all_or_none": False,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_FOK(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "FOK",
                "all_or_none": True,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_FOK_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "FOK",
                "all_or_none": False,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_GTD(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTD",
                "all_or_none": True,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_buy_Limit_GTD_none(self):
        response = client.post(
            "/buy",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTD",
                "all_or_none": False,
                "lower_bound": 50,
                "upper_bound": 70,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_DAY(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "Day",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_DAY_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "Day",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_GTC(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTC",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_GTC_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTC",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_IOC(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "IOC",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_IOC_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "IOC",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_FOK(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "FOK",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_FOK_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "FOK",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_GTD(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTD",
                "all_or_none": True,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Market_GTD_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Market",
                "order_behaviour": "GTD",
                "all_or_none": False,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_DAY(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "DAY",
                "all_or_none": True,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_DAY_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "DAY",
                "all_or_none": False,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_GTC(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTC",
                "all_or_none": True,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_GTC_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTC",
                "all_or_none": False,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_IOC(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "IOC",
                "all_or_none": True,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_IOC_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "IOC",
                "all_or_none": False,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_FOK(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "FOK",
                "all_or_none": True,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_FOK_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "FOK",
                "all_or_none": False,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_GTD(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTD",
                "all_or_none": True,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def test_stock_sell_Limit_GTD_none(self):
        response = client.post(
            "/sell",
            json={
                "user_id": 1,
                "stock_id": self.stock_id,
                "total": 5,
                "order_type": "Limit",
                "order_behaviour": "GTD",
                "all_or_none": False,
                "lower_bound": 100,
                "upper_bound": 150,
            },
        )
        self.assertTrue(response.status_code)

    def tearDown(self):
        self.client.loop_stop()
