package esd.weather.models;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Location {
    
    @JsonProperty("lat")
    private float latitude;
    @JsonProperty("long")
    private float longitude;
    private String name;
    private String region;
    private String country;
    private String tz_id;
    private int localtime_epoch;
    private LocalDateTime localtime;

    public Location(float latitude, float longitude, String name, String region, String country, String tz_id, int localtime_epoch,
            String localtime) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.name = name;
        this.region = region;
        this.country = country;
        this.tz_id = tz_id;
        this.localtime_epoch = localtime_epoch;
        this.localtime = LocalDateTime.parse(localtime, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
    }

    public float getLatitude() {
        return latitude;
    }

    public float getLongitude() {
        return longitude;
    }

    public String getName() {
        return name;
    }

    public String getRegion() {
        return region;
    }

    public String getCountry() {
        return country;
    }

    public String getTz_id() {
        return tz_id;
    }

    public int getLocaltime_epoch() {
        return localtime_epoch;
    }

    public LocalDateTime getLocaltime() {
        return localtime;
    }

    
}
