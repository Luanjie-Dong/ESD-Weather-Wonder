package esd.emergencyweather.models;

public class Alerts {
    private Alert[] alert;

    public Alerts(Alert[] alert) {
        this.alert = alert;
    }

    public Alert[] getAlert() {
        return alert;
    }
}
