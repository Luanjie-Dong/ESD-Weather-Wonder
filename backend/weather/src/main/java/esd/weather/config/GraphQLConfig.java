package esd.weather.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import esd.weather.resolvers.WeatherResolver;

@Configuration
public class GraphQLConfig {
    @Bean
    WeatherResolver weatherResolver() {
        return new WeatherResolver();
    }
}
