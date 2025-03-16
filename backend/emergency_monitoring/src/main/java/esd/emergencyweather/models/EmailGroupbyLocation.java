package esd.emergencyweather.models;

public class EmailGroupbyLocation {
    private String country;
    private String state;
    private String city;
    private String[] emails;

    public EmailGroupbyLocation(String country, String state, String city, String emails) {
        this.country = country;
        this.state = state;
        this.city = city;
        this.emails = emails.split(", ");
    }

    public String getCountry() {
        return country;
    }

    public String getState() {
        return state;
    }

    public String getCity() {
        return city;
    }

    public String[] getEmails() {
        return emails;
    }
}
