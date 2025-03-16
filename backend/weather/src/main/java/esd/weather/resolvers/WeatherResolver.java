package esd.weather.resolvers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import esd.weather.MainWrapper;
import esd.weather.models.AlertDAO;
import esd.weather.models.CurrentDAO;
import esd.weather.models.ForecastDAO;

@Controller
public class WeatherResolver {

    @Autowired
    private MainWrapper mainWrapper;

    @QueryMapping
    public ForecastDAO getForecast(
        @Argument String country, 
        @Argument String state, 
        @Argument String city, 
        @Argument String neighbourhood
    ) {
        if (country == null || country.isEmpty() || state == null || state.isEmpty() || city == null || city.isEmpty() || neighbourhood == null || neighbourhood.isEmpty()) {
            throw new RuntimeException("All location parameters are required.");
        }
        try {
            return mainWrapper.getForecast(country, state, city, neighbourhood);
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch forecast data", e);
        }
    }

    @QueryMapping
    public CurrentDAO getCurrent(
        @Argument String country, 
        @Argument String state, 
        @Argument String city, 
        @Argument String neighbourhood
    ) {
        if (country == null || country.isEmpty() || state == null || state.isEmpty() || city == null || city.isEmpty() || neighbourhood == null || neighbourhood.isEmpty()) {
            throw new RuntimeException("All location parameters are required.");
        }
        try {
            return mainWrapper.getCurrent(country, state, city, neighbourhood);
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch current data", e);
        }
    }

    @QueryMapping
    public AlertDAO getAlerts(
        @Argument String country, 
        @Argument String state, 
        @Argument String city
    ) {
        if (country == null || country.isEmpty() || state == null || state.isEmpty() || city == null || city.isEmpty()) {
            throw new RuntimeException("Country, state, and city are required.");
        }
        try {
            return mainWrapper.getAlerts(country, state, city);
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch alerts data", e);
        }
    }
}
