import sys
import os
from dotenv import load_dotenv
import requests
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

# Load environment variables at the start
load_dotenv()
# Note: Key name should match exactly what's in your .env file (case-sensitive)
weather_key = os.environ.get('WEATHER_KEY')  # Changed 'weather_key' to 'WEATHER_KEY'

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        self.setWindowTitle("Weather App")
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create widgets
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setObjectName("cityInput")
        
        self.search_button = QPushButton("Get Weather", self)
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(self.get_weather)
        
        self.weather_label = QLabel("Weather information will appear here")
        self.weather_label.setObjectName("weatherLabel")
        self.weather_label.setAlignment(Qt.AlignCenter)
        
        # Apply stylesheet (unchanged)
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
            }
            QLineEdit#cityInput {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit#cityInput:focus {
                border-color: #2980b9;
                background-color: #ecf0f1;
            }
            QPushButton#searchButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton#searchButton:hover {
                background-color: #2980b9;
            }
            QPushButton#searchButton:pressed {
                background-color: #20638f;
            }
            QLabel#weatherLabel {
                font-size: 18px;
                color: #2c3e50;
                padding: 15px;
                background-color: #dfe6e9;
                border-radius: 5px;
            }
        """)
        
        # Add widgets to layout
        layout.addWidget(self.city_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.weather_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_weather(self):
        city = self.city_input.text()
        if city:
            try:
                api_key = os.environ.get('WEATHER_KEY')  # Changed to 'WEATHER_KEY'
                if not api_key:
                    self.weather_label.setText("API key not found!")
                    return
                    
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                response.raise_for_status()  # Raises exception for HTTP errors
                data = response.json()
                
                if data["cod"] == 200:  # Success code from OpenWeatherMap
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    self.weather_label.setText(f"Temperature: {temp}°C\nDescription: {desc}")
                else:
                    self.weather_label.setText(f"Error: {data.get('message', 'City not found')}")
            except requests.exceptions.RequestException as e:
                self.display_error(f"Request Error: {str(e)}")
            except Exception as e:
                self.display_error(f"Unexpected Error: {str(e)}")
        else:
            self.weather_label.setText("Please enter a city name")
    
    def display_error(self, response):
        self.weather_label.setStyleSheet("font-size: 20px")  # This overrides previous styling
        self.weather_label.setText(response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())