class Subject:
    # Both of the following two methods take an
    # observer as an argument; that is, the observer
    # to be registered ore removed.
    def registerObserver(observer):
        pass
    def removeObserver(observer):
        pass
    
    # This method is called to notify all observers
    # when the Subject's state (measurements) has changed.
    def notifyObservers():
        pass
    
# The observer class is implemented by all observers,
# so they all have to implemented the update() method. Here
# we're following Mary and Sue's lead and 
# passing the measurements to the observers.
class Observer:
    def update(self, temp, humidity, pressure):
        pass
 
# WeatherData now implements the subject interface.
class WeatherData(Subject):
    
    def __init__(self):        
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
    
    
    def registerObserver(self, observer):
        # When an observer registers, we just 
        # add it to the end of the list.
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        # When an observer wants to un-register,
        # we just take it off the list.
        self.observers.remove(observer)
    
    def notifyObservers(self):
        # We notify the observers when we get updated measurements 
        # from the Weather Station.
        for ob in self.observers:
            ob.update(self.temperature, self.humidity, self.pressure)
    
    def measurementsChanged(self):
        self.notifyObservers()
    
    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        
        self.measurementsChanged()
    
    # other WeatherData methods here.
 
class CurrentConditionsDisplay(Observer):
    
    def __init__(self, weatherData):        
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        
        self.weatherData = weatherData # save the ref in an attribute.
        weatherData.registerObserver(self) # register the observer 
                                           # so it gets data updates.
    def update(self, temperature, humidity, pressure):
        self.temeprature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()
        
    def display(self):
        print("Current conditions:", self.temperature, 
              "F degrees and", self.humidity,"[%] humidity",
              "and pressure", self.pressure)
        
# TODO: implement StatisticsDisplay class and ForecastDisplay class.
class StatiticsDisplay(Observer):
    
    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.temperature_avg = 0
        self.humidity_avg = 0
        self.pressure_avg = 0
        self.temperature_min = 0
        self.humidity_min = 0
        self.pressure_min = 0
        self.temperature_max = 0
        self.humidity_max = 0
        self.pressure_max = 0

        # save the ref in an attribute.
        weatherData.registerObserver(self)

    def calculate_avg(self):
        self.temperature_avg = (self.temperature_avg * 9 + self.temperature) / 10
        self.humidity_avg = (self.humidity_avg * 9 + self.humidity) / 10
        self.pressure_avg = (self.pressure_avg * 9 + self.pressure) / 10
    def calculate_min(self):
        if self.temperature_min == 0:
            self.temperature_min = self.temperature
        elif self.temperature < self.temperature_min:
            self.temperature_min = self.temperature
        if self.humidity_min == 0:
            self.humidity_min = self.humidity
        elif self.humidity < self.humidity_min:
            self.humidity_min = self.humidity
        if self.pressure_min == 0:
            self.pressure_min = self.pressure
        elif self.pressure < self.pressure_min:
            self.pressure_min = self.pressure
    def calculate_max(self):
        if self.temperature_max == 0:
            self.temperature_max = self.temperature
        elif self.temperature > self.temperature_max:
            self.temperature_max = self.temperature
        if self.humidity_max == 0:
            self.humidity_max = self.humidity
        elif self.humidity > self.humidity_max:
            self.humidity_max = self.humidity
        if self.pressure_max == 0:
            self.pressure_max = self.pressure
        elif self.pressure > self.pressure_max:
            self.pressure_max = self.pressure

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.calculate_avg()
        self.calculate_min()
        self.calculate_max()
        self.display()

    def display(self):
        print("Current Statistics:")
        print("Temperature:")
        print("\tAvg:", self.temperature_avg)
        print("\tMin:", self.temperature_min)
        print("\tMax:", self.temperature_max)
        print("Humidity:")
        print("\tAvg:", self.humidity_avg)
        print("\tMin:", self.humidity_min)
        print("\tMax:", self.humidity_max)
        print("Pressure:")
        print("\tAvg:", self.pressure_avg)
        print("\tMin:", self.pressure_min)
        print("\tMax:", self.pressure_max)

class ForecastDisplay:
    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.weatherData = weatherData
        self.weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.temperature = self.weatherData.temperature + 0.11 * self.weatherData.humidity + 0.2 * self.weatherData.pressure
        self.humidity = self.weatherData.humidity - 0.9 * self.weatherData.humidity
        self.pressure = self.weatherData.pressure + 0.01 * self.weatherData.temperature - 0.21 * self.weatherData.pressure
        self.display()

    def display(self):
        print("Forecast conditions:", self.temperature, "F degrees and", self.humidity,"[%] humidity",
              "and pressure", self.pressure)
    
    
class WeatherStation:
    def main(self):
        weather_data = WeatherData()
        current_display = CurrentConditionsDisplay(weather_data)
        
        # TODO: Create two objects from StatisticsDisplay class and 
        # ForecastDisplay class. Also, register them to the concrete instance
        # of the Subject class so they get the measurements' updates.
        display_statistics = StatiticsDisplay(weather_data)
        display_forecast = ForecastDisplay(weather_data)
        # The StatisticsDisplay class should keep track of the min/average/max
        # measurements and display them.
        
        # The ForecastDisplay class shows the weather forecast based on the current
        # temperature, humidity and pressure. Use the following formulas :
        # forcast_temp = temperature + 0.11 * humidity + 0.2 * pressure
        # forcast_humadity = humidity - 0.9 * humidity
        # forcast_pressure = pressure + 0.1 * temperature - 0.21 * pressure
        
        weather_data.setMeasurements(80, 65,30.4)
        weather_data.setMeasurements(82, 70,29.2)
        weather_data.setMeasurements(78, 90,29.2)
        
        # un-register the observer
        weather_data.removeObserver(current_display)
        weather_data.setMeasurements(120, 100,1000)
    
        
 
if __name__ == "__main__":
    w = WeatherStation()
    w.main()
