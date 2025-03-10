package esd.weather;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import esd.weather.models.*;

import java.net.URI;

@ComponentScan(basePackages = "esd.weather")
@Service
public class MainWrapper {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${weatherapi.url}")
    private String url;

    @Value("${weatherapi.key}")
    private String apiKey;

    public ForecastDAO getForecast(String country, String state, String city, String neighbourhood) {
        URI request = UriComponentsBuilder.fromUriString(url)
            .path("/v1/forecast.json")
            .queryParam("key", apiKey)
            .queryParam("q", neighbourhood + ", " + city + ", " + state + ", " + country)
            .build()
            .encode()
            .toUri();
        return restTemplate.getForObject(request, ForecastDAO.class);
    }

    public CurrentDAO getCurrent(String country, String state, String city, String neighbourhood) {
        URI request = UriComponentsBuilder.fromUriString(url)
        .path("/v1/current.json")
        .queryParam("key", apiKey)
        .queryParam("q", neighbourhood + ", " + city + ", " + state + ", " + country)
        .queryParam("aqi", "no")
        .build()
        .encode()
        .toUri();
        return restTemplate.getForObject(request, CurrentDAO.class);
    }

    public AlertDAO getAlerts(String country, String state, String city) {
        URI request = UriComponentsBuilder.fromUriString(url)
            .path("/v1/alerts.json")
            .queryParam("key", apiKey)
            .queryParam("q", city + ", " + state + ", " + country)
            .build()
            .encode()
            .toUri();
        return restTemplate.getForObject(request, AlertDAO.class);
    }
}
