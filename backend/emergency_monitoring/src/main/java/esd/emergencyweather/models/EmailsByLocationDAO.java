package esd.emergencyweather.models;

public class EmailsByLocationDAO {
    private int code;
    private int count;
    private EmailGroupbyLocation[] emails_by_location;

    public EmailsByLocationDAO(int code, int count, EmailGroupbyLocation[] emails_by_location) {
        this.code = code;
        this.count = count;
        this.emails_by_location = emails_by_location;
    }

    public int getCode() {
        return code;
    }

    public int getCount() {
        return count;
    }

    public EmailGroupbyLocation[] getEmails_by_location() {
        return emails_by_location;
    }
}
