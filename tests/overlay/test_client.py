import unittest
from aboutlife.overlay import client


class TestClient(unittest.TestCase):
    def test_get_state(self):
        resp = client.get_state()
        self.assertIsNotNone(resp)

    def test_post_start_work_cycle(self):
        resp = client.post_start_work_cycle("working on my tesis")
        self.assertTrue(resp)


if __name__ == "__main__":
    unittest.main()
