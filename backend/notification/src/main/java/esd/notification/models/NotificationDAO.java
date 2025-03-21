package esd.notification.models;

public class NotificationDAO {
    private String recipients;
    private String subject;
    private String content;
    private boolean bcc = false;
    
    public NotificationDAO() {}
    
    public NotificationDAO(String recipients, String subject, String content) {
        this.recipients = recipients;
        this.subject = subject;
        this.content = content;
    }

    public String getRecipients() {
        return recipients;
    }

    public String getSubject() {
        return subject;
    }

    public String getContent() {
        return content;
    }

    public boolean isBcc() {
        return bcc;
    }

    public void setBcc(boolean isBcc) {
        this.bcc = isBcc;
    }
}
