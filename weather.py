import sys
import requests
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

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
        self.city_input.setObjectName("cityInput")  # Set object name for specific styling
        
        self.search_button = QPushButton("Get Weather", self)
        self.search_button.setObjectName("searchButton")  # Set object name for specific styling
        self.search_button.clicked.connect(self.get_weather)
        
        self.weather_label = QLabel("Weather information will appear here")
        self.weather_label.setObjectName("weatherLabel")  # Set object name for specific styling
        self.weather_label.setAlignment(Qt.AlignCenter)
        
        # Apply stylesheet to the entire widget
        self.setStyleSheet("""
            /* Global styles */
            QWidget {
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
            }
            
            /* Style for QLineEdit (city input) */
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
            
            /* Style for QPushButton (search button) */
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
            
            /* Style for QLabel (weather display) */
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
        layout.addStretch()  # Adds flexible space at the bottom
        
        # Set layout
        self.setLayout(layout)
    
    def get_weather(self):
        city = self.city_input.text()
        if city:
            try:
                api_key = "e7f94475f0a798c607d435e94037bdcc"
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                
                if data["cod"] == 200:
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    self.weather_label.setText(f"Temperature: {temp}°C\nDescription: {desc}")
                else:
                    self.weather_label.setText("City not found!")
            except Exception as e :
                self.display_error(f"Request Error: \n {e}")
        else:
            self.weather_label.setText("Please enter a city name")
    
    def display_error(self, response):
        self.weather_label.setStyleSheet("font-size: 20px")
        self.weather_label.setText(response)
      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())