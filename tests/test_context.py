import unittest
from aboutlife.context import Context


class TestContext(unittest.TestCase):
    def test_get_state(self):
        for i in range(-1, 25):
            is_late = Context.is_late_hour(i)

            if i in range(5, 11):
                self.assertFalse(is_late)

            if i in range(12 + 5, 12 + 7):
                self.assertFalse(is_late)

            if i in range(20, 25):
                self.assertTrue(is_late)


if __name__ == "__main__":
    unittest.main()
