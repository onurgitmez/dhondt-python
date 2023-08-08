import unittest
import pandas as pd
from dhondt import simulate_election

class TestSimulateElection(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            'DistrictName': ['DistrictA', 'DistrictB'],
            'Party1Vote': [100, 200],
            'Party2Vote': [150, 50],
            'NumberofSeats': [1, 2]
        })

    def test_basic_simulation(self):
        results = simulate_election(self.sample_data, "DistrictName", "NumberofSeats", ["Party1Vote", "Party2Vote"], threshold=0)
        print("Returned Results:", results)
        self.assertEqual(results['totals']['Party1Vote'], 2)
        self.assertEqual(results['totals']['Party2Vote'], 1)

    def test_threshold_functionality(self):
        df = pd.DataFrame({
            'DistrictName': ['DistrictA'],
            'Party1Vote': [90],
            'Party2Vote': [10],
            'NumberofSeats': [1]
        })
        results = simulate_election(df, "DistrictName", "NumberofSeats", ["Party1Vote", "Party2Vote"], threshold=0.15)
        self.assertEqual(results['totals']['Party1Vote'], 1)
        self.assertEqual(results['totals']['Party2Vote'], 0)


    def test_tie_scenario(self):
        df = pd.DataFrame({
            'DistrictName': ['DistrictA'],
            'Party1Vote': [500],
            'Party2Vote': [500],
            'NumberofSeats': [1]
        })
        results = simulate_election(df, "DistrictName", "NumberofSeats", ["Party1Vote", "Party2Vote"], threshold=0)
        self.assertEqual(results['totals']['Party1Vote'] + results['totals']['Party2Vote'], 1)



   
if __name__ == '__main__':
    unittest.main()
