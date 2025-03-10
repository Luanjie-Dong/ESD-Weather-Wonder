package esd.weather.models;

import java.time.LocalDate;

public class ForecastDay {

    private LocalDate date;
    private int date_epoch;
    private Day day;
    private Astro astro;
    private Hour[] hour;

    public ForecastDay(LocalDate date, int date_epoch, Day day, Astro astro, Hour[] hour) {
        this.date = date;
        this.date_epoch = date_epoch;
        this.day = day;
        this.astro = astro;
        this.hour = hour;
    }

    public LocalDate getDate() {
        return date;
    }

    public int getDate_epoch() {
        return date_epoch;
    }

    public Day getDay() {
        return day;
    }

    public Astro getAstro() {
        return astro;
    }

    public Hour[] getHour() {
        return hour;
    }

    
}
