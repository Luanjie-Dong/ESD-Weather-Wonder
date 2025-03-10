package esd.weather.models;

public class ForecastDAO {
    
    private Location location;
    private Current current;
    private Forecast forecast;

    public ForecastDAO(Location location, Current current, Forecast forecast) {
        this.location = location;
        this.current = current;
        this.forecast = forecast;
    }

    public Location getLocation() {
        return location;
    }

    public Current getCurrent() {
        return current;
    }

    public Forecast getForecast() {
        return forecast;
    }
}
