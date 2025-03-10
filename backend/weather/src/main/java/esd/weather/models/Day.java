package esd.weather.models;

public class Day {
    private float maxtemp_c;
    private float maxtemp_f;
    private float mintemp_c;
    private float mintemp_f;
    private float avgtemp_c;
    private float avgtemp_f;
    private float maxwind_kph;
    private float maxwind_mph;
    private float totalprecip_mm;
    private float totalprecip_in;
    private float totalsnow_cm;
    private float avgvis_km;
    private float avgvis_miles;
    private int avghumidity;
    private String condition_text;
    private String condition_icon;
    private int condition_code;
    private float uv;
    private int daily_will_it_rain;
    private int daily_will_it_snow;
    private int daily_chance_of_rain;
    private int daily_chance_of_snow;

    public Day(float maxtemp_c, float maxtemp_f, float mintemp_c, float mintemp_f, float avgtemp_c, float avgtemp_f,
            float maxwind_kph, float maxwind_mph, float totalprecip_mm, float totalprecip_in, float totalsnow_cm,
            float avgvis_km, float avgvis_miles, int avghumidity, String condition_text, String condition_icon,
            int condition_code, float uv, int daily_will_it_rain, int daily_will_it_snow, int daily_chance_of_rain,
            int daily_chance_of_snow) {
        this.maxtemp_c = maxtemp_c;
        this.maxtemp_f = maxtemp_f;
        this.mintemp_c = mintemp_c;
        this.mintemp_f = mintemp_f;
        this.avgtemp_c = avgtemp_c;
        this.avgtemp_f = avgtemp_f;
        this.maxwind_kph = maxwind_kph;
        this.maxwind_mph = maxwind_mph;
        this.totalprecip_mm = totalprecip_mm;
        this.totalprecip_in = totalprecip_in;
        this.totalsnow_cm = totalsnow_cm;
        this.avgvis_km = avgvis_km;
        this.avgvis_miles = avgvis_miles;
        this.avghumidity = avghumidity;
        this.condition_text = condition_text;
        this.condition_icon = condition_icon;
        this.condition_code = condition_code;
        this.uv = uv;
        this.daily_will_it_rain = daily_will_it_rain;
        this.daily_will_it_snow = daily_will_it_snow;
        this.daily_chance_of_rain = daily_chance_of_rain;
        this.daily_chance_of_snow = daily_chance_of_snow;
    }

    public float getMaxtemp_c() {
        return maxtemp_c;
    }

    public float getMaxtemp_f() {
        return maxtemp_f;
    }

    public float getMintemp_c() {
        return mintemp_c;
    }

    public float getMintemp_f() {
        return mintemp_f;
    }

    public float getAvgtemp_c() {
        return avgtemp_c;
    }

    public float getAvgtemp_f() {
        return avgtemp_f;
    }

    public float getMaxwind_kph() {
        return maxwind_kph;
    }

    public float getMaxwind_mph() {
        return maxwind_mph;
    }

    public float getTotalprecip_mm() {
        return totalprecip_mm;
    }

    public float getTotalprecip_in() {
        return totalprecip_in;
    }

    public float getTotalsnow_cm() {
        return totalsnow_cm;
    }

    public float getAvgvis_km() {
        return avgvis_km;
    }

    public float getAvgvis_miles() {
        return avgvis_miles;
    }

    public int getAvghumidity() {
        return avghumidity;
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

    public float getUv() {
        return uv;
    }

    public int getDaily_will_it_rain() {
        return daily_will_it_rain;
    }

    public int getDaily_will_it_snow() {
        return daily_will_it_snow;
    }

    public int getDaily_chance_of_rain() {
        return daily_chance_of_rain;
    }

    public int getDaily_chance_of_snow() {
        return daily_chance_of_snow;
    }

    
}
