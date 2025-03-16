package esd.emergencyweather.models;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class Astro {
    private LocalTime sunrise;
    private LocalTime sunset;
    private LocalTime moonrise;
    private LocalTime moonset;
    private String moon_phase;
    private float moon_illumination;
    private int is_moon_up;
    private int is_sun_up;
    
    public Astro(String sunrise, String sunset, String moonrise, String moonset,
            String moon_phase, float moon_illumination, int is_moon_up, int is_sun_up) {
        this.sunrise = LocalTime.parse(sunrise, DateTimeFormatter.ofPattern("hh:mm a"));
        this.sunset = LocalTime.parse(sunset, DateTimeFormatter.ofPattern("hh:mm a"));
        this.moonrise = LocalTime.parse(moonrise, DateTimeFormatter.ofPattern("hh:mm a"));
        this.moonset = LocalTime.parse(moonset, DateTimeFormatter.ofPattern("hh:mm a"));
        this.moon_phase = moon_phase;
        this.moon_illumination = moon_illumination;
        this.is_moon_up = is_moon_up;
        this.is_sun_up = is_sun_up;
    }

    public LocalTime getSunrise() {
        return sunrise;
    }

    public LocalTime getSunset() {
        return sunset;
    }

    public LocalTime getMoonrise() {
        return moonrise;
    }

    public LocalTime getMoonset() {
        return moonset;
    }

    public String getMoon_phase() {
        return moon_phase;
    }

    public float getMoon_illumination() {
        return moon_illumination;
    }

    public int getIs_moon_up() {
        return is_moon_up;
    }

    public int getIs_sun_up() {
        return is_sun_up;
    }

    
}
