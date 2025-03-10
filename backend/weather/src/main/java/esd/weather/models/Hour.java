package esd.weather.models;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Hour {
    private int time_epoch;
    private LocalDateTime time;
    private float temp_c;
    private float temp_f;
    private String condition_text;
    private String condition_icon;
    private int condition_code;
    private float wind_mph;
    private float wind_kph;
    private int wind_degree;
    private String wind_dir;
    private float pressure_mb;
    private float pressure_in;
    private float precip_mm;
    private float precip_in;
    private float snow_cm;
    private int humidity;
    private int cloud;
    private float feelslike_c;
    private float feelslike_f;
    private float windchill_c;
    private float windchill_f;
    private float heatindex_c;
    private float heatindex_f;
    private float dewpoint_c;
    private float dewpoint_f;
    private int will_it_rain;
    private int will_it_snow;
    private int is_day;
    private float vis_km;
    private float vis_miles;
    private int chance_of_rain;
    private int chance_of_snow;
    private float gust_mph;
    private float gust_kph;
    private float uv;
    private float short_rad;
    private float diff_rad;

    public Hour(int time_epoch, String time, float temp_c, float temp_f, String condition_text,
            String condition_icon, int condition_code, float wind_mph, float wind_kph, int wind_degree, String wind_dir,
            float pressure_mb, float pressure_in, float precip_mm, float precip_in, float snow_cm, int humidity,
            int cloud, float feelslike_c, float feelslike_f, float windchill_c, float windchill_f, float heatindex_c,
            float heatindex_f, float dewpoint_c, float dewpoint_f, int will_it_rain, int will_it_snow, int is_day,
            float vis_km, float vis_miles, int chance_of_rain, int chance_of_snow, float gust_mph, float gust_kph,
            float uv, float short_rad, float diff_rad) {
        this.time_epoch = time_epoch;
        this.time = LocalDateTime.parse(time, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
        this.temp_c = temp_c;
        this.temp_f = temp_f;
        this.condition_text = condition_text;
        this.condition_icon = condition_icon;
        this.condition_code = condition_code;
        this.wind_mph = wind_mph;
        this.wind_kph = wind_kph;
        this.wind_degree = wind_degree;
        this.wind_dir = wind_dir;
        this.pressure_mb = pressure_mb;
        this.pressure_in = pressure_in;
        this.precip_mm = precip_mm;
        this.precip_in = precip_in;
        this.snow_cm = snow_cm;
        this.humidity = humidity;
        this.cloud = cloud;
        this.feelslike_c = feelslike_c;
        this.feelslike_f = feelslike_f;
        this.windchill_c = windchill_c;
        this.windchill_f = windchill_f;
        this.heatindex_c = heatindex_c;
        this.heatindex_f = heatindex_f;
        this.dewpoint_c = dewpoint_c;
        this.dewpoint_f = dewpoint_f;
        this.will_it_rain = will_it_rain;
        this.will_it_snow = will_it_snow;
        this.is_day = is_day;
        this.vis_km = vis_km;
        this.vis_miles = vis_miles;
        this.chance_of_rain = chance_of_rain;
        this.chance_of_snow = chance_of_snow;
        this.gust_mph = gust_mph;
        this.gust_kph = gust_kph;
        this.uv = uv;
        this.short_rad = short_rad;
        this.diff_rad = diff_rad;
    }

    public int getTime_epoch() {
        return time_epoch;
    }

    public LocalDateTime getTime() {
        return time;
    }

    public float getTemp_c() {
        return temp_c;
    }

    public float getTemp_f() {
        return temp_f;
    }

    public String getCondition_text() {
        return condition_text;
    }

    public String getCondition_icon() {
        return condition_icon;
    }

    public int getCondition_code() {
        return condition_code;
    }

    public float getWind_mph() {
        return wind_mph;
    }

    public float getWind_kph() {
        return wind_kph;
    }

    public int getWind_degree() {
        return wind_degree;
    }

    public String getWind_dir() {
        return wind_dir;
    }

    public float getPressure_mb() {
        return pressure_mb;
    }

    public float getPressure_in() {
        return pressure_in;
    }

    public float getPrecip_mm() {
        return precip_mm;
    }

    public float getPrecip_in() {
        return precip_in;
    }

    public float getSnow_cm() {
        return snow_cm;
    }

    public int getHumidity() {
        return humidity;
    }

    public int getCloud() {
        return cloud;
    }

    public float getFeelslike_c() {
        return feelslike_c;
    }

    public float getFeelslike_f() {
        return feelslike_f;
    }

    public float getWindchill_c() {
        return windchill_c;
    }

    public float getWindchill_f() {
        return windchill_f;
    }

    public float getHeatindex_c() {
        return heatindex_c;
    }

    public float getHeatindex_f() {
        return heatindex_f;
    }

    public float getDewpoint_c() {
        return dewpoint_c;
    }

    public float getDewpoint_f() {
        return dewpoint_f;
    }

    public int getWill_it_rain() {
        return will_it_rain;
    }

    public int getWill_it_snow() {
        return will_it_snow;
    }

    public int getIs_day() {
        return is_day;
    }

    public float getVis_km() {
        return vis_km;
    }

    public float getVis_miles() {
        return vis_miles;
    }

    public int getChance_of_rain() {
        return chance_of_rain;
    }

    public int getChance_of_snow() {
        return chance_of_snow;
    }

    public float getGust_mph() {
        return gust_mph;
    }

    public float getGust_kph() {
        return gust_kph;
    }

    public float getUv() {
        return uv;
    }

    public float getShort_rad() {
        return short_rad;
    }

    public float getDiff_rad() {
        return diff_rad;
    }

    
}
