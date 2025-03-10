package esd.weather;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import esd.weather.models.*;

@RestController
public class MainController {

    @Autowired
    private MainWrapper mainWrapper;
    
    @GetMapping("/")
    public String ping() {
        return "Microservice is up and running!";
    }

    @GetMapping("/forecast")
    public ForecastDay getForecast(
        @RequestParam("country") String country, 
        @RequestParam("state") String state, 
        @RequestParam("city") String city, 
        @RequestParam("neighbourhood") String neighbourhood
        ) {
        ForecastDAO forecastDAO = mainWrapper.getForecast(country, state, city, neighbourhood);
        return forecastDAO.getForecast().getForecastDay()[0];
    }

    @GetMapping("/current")
    public Current getCurrent(
        @RequestParam("country") String country, 
        @RequestParam("state") String state, 
        @RequestParam("city") String city, 
        @RequestParam("neighbourhood") String neighbourhood
        ) {
        CurrentDAO currentDAO = mainWrapper.getCurrent(country, state, city, neighbourhood);
        return currentDAO.getCurrent();
    }

    @GetMapping("/alerts")
    public Alert[] getAlerts(
        @RequestParam("country") String country, 
        @RequestParam("state") String state, 
        @RequestParam("city") String city
        ) {
        AlertDAO alertDAO = mainWrapper.getAlerts(country, state, city);
        return alertDAO.getAlerts().getAlert();
    }
}
