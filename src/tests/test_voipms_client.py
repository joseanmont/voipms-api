import unittest
from voipms_api import VoipMsClient

class TestVoIPmsClient(unittest.TestCase):

    def test_connection(self):
        """
        Tests if the credentials and IP address are correct.
        """
        client = VoipMsClient()
        result = client.test_connection()
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    
    unittest.main()