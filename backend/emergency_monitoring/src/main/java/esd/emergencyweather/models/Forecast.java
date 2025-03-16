package esd.emergencyweather.models;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Forecast {

    private ForecastDay[] forecastDay;

    public Forecast(ForecastDay[] forecastDay) {
        this.forecastDay = forecastDay;
    }

    public ForecastDay[] getForecastDay() {
        return forecastDay;
    }
}

