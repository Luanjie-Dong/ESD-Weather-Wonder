package esd.weather.models;

public class CurrentDAO {
    private Location location;
    private Current current;

    public CurrentDAO(Location location, Current current) {
        this.location = location;
        this.current = current;
    }

    public Location getLocation() {
        return location;
    }

    public Current getCurrent() {
        return current;
    }
}
