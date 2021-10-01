import unittest
from src.opensea import OpenseaAPI

class OpenseaAPITest(unittest.TestCase):

    def setUp(self):
        self.opensea = OpenseaAPI(
            asset_owner="0x9c847ce765a48701fba267366eefa12606780d72",
            base_api="https://api.opensea.io/api/v1"
        )
        self.collection = 'monsters-evolution'

    def test_get_collections(self):
       status_code, response = self.opensea.get_collections()
       self.assertEqual(status_code, 200) 

    def test__get_assets(self):
       status_code, response = self.opensea._get_assets()
       self.assertEqual(status_code, 200) 

    def test__get_assets_with_collection(self):
       status_code, response = self.opensea._get_assets(collection=self.collection)
       self.assertEqual(status_code, 200) 

    def test_get_assets(self):
        assets = self.opensea.get_assets()
        self.assertTrue(type(assets) == list)

    def test_get_assets_with_collection(self):
        assets = self.opensea.get_assets(collection=self.collection)
        self.assertTrue(type(assets) == list)
        self.assertEqual(len(assets), 1000)


if __name__ == '__main__':
    unittest.main()