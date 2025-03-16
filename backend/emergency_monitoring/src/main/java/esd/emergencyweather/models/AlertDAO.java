package esd.emergencyweather.models;

public class AlertDAO {
    private Location location;
    private Alerts alerts;

    public AlertDAO(Location location, Alerts alerts) {
        this.location = location;
        this.alerts = alerts;
    }

    public Location getLocation() {
        return location;
    }

    public Alerts getAlerts() {
        return alerts;
    }
}
