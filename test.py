import unittest
import sys
import time
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from weather import WeatherApp  # Import your WeatherApp class from weather.py

# Required for PyQt5 tests
app = QApplication(sys.argv)

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None
        self._elapsed_time = 0
        
    def startTestRun(self):
        """Start timing when tests begin"""
        self.start_time = time.time()
        super().startTestRun()
        
    def stopTestRun(self):
        """Calculate elapsed time when tests finish"""
        if self.start_time is not None:
            self._elapsed_time = time.time() - self.start_time
        super().stopTestRun()

    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{test} ------------------------ OK")
        print(f"{test._testMethodDoc.strip()}\n")
        
    def startTest(self, test):
        super().startTest(test)

    def printErrors(self):
        # Override to prevent extra error output unless needed
        pass

class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(resultclass=CustomTestResult, *args, **kwargs)

class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        """Set up a fresh instance of WeatherApp before each test"""
        self.weather_app = WeatherApp()
        
    def tearDown(self):
        """Clean up after each test"""
        self.weather_app.close()
        
    def test_initialization(self):
        """Test that the app initializes correctly"""
        self.assertEqual(self.weather_app.windowTitle(), "Weather App")
        self.assertIsNotNone(self.weather_app.layout())
        self.assertIsNotNone(self.weather_app.city_input)
        self.assertIsNotNone(self.weather_app.search_button)
        self.assertIsNotNone(self.weather_app.weather_label)
        
    @patch('weather.requests.get')
    def test_get_weather_success(self, mock_get):
        """Test successful weather API call"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cod": 200,
            "main": {"temp": 20.5, "feels_like": 21.0, "humidity": 65},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.5}
        }
        mock_get.return_value = mock_response
        self.weather_app.city_input.setText("London")
        self.weather_app.get_weather()
        label_text = self.weather_app.weather_label.text()
        self.assertIn("20.5", label_text)
        self.assertIn("clear sky", label_text.lower())
        
    @patch('weather.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        """Test handling of invalid city"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "cod": "404",
            "message": "city not found"
        }
        mock_get.return_value = mock_response
        self.weather_app.city_input.setText("InvalidCityXYZ")
        self.weather_app.get_weather()
        label_text = self.weather_app.weather_label.text()
        self.assertIn("not found", label_text.lower())
        
    def test_get_weather_empty_input(self):
        """Test handling of empty input"""
        self.weather_app.city_input.clear()
        self.weather_app.get_weather()
        label_text = self.weather_app.weather_label.text()
        self.assertTrue("error" in label_text.lower() or "enter" in label_text.lower())
        
    @patch('weather.requests.get', side_effect=Exception("Network error"))
    def test_get_weather_network_error(self, mock_get):
        """Test handling of network errors"""
        self.weather_app.city_input.setText("London")
        self.weather_app.get_weather()
        label_text = self.weather_app.weather_label.text()
        self.assertIn("error", label_text.lower())

if __name__ == '__main__':
    runner = CustomTestRunner(verbosity=0)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherApp)
    result = runner.run(suite)
    print("----------------------------------------------------------------------")
    print(f"Ran {result.testsRun} tests in {result._elapsed_time:.3f}s")
    print("\nOK" if result.wasSuccessful() else "\nFAILED")