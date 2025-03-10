package esd.weather.models;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Alert {
    private String headline;
    private String msgType;
    private String severity;
    private String urgency;
    private String areas;
    private String category;
    private String certainty;
    private String event;
    private String note;
    private LocalDateTime effective;
    private LocalDateTime expires;
    private String desc;
    private String instruction;

    public Alert(String headline, String msgType, String severity, String urgency, String areas, String category,
            String certainty, String event, String note, String effective, String expires, String desc,
            String instruction) {
        this.headline = headline;
        this.msgType = msgType;
        this.severity = severity;
        this.urgency = urgency;
        this.areas = areas;
        this.category = category;
        this.certainty = certainty;
        this.event = event;
        this.note = note;
        this.effective = LocalDateTime.parse(effective, DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        this.expires = LocalDateTime.parse(expires, DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        this.desc = desc;
        this.instruction = instruction;
    }

    public String getHeadline() {
        return headline;
    }

    public String getMsgType() {
        return msgType;
    }

    public String getSeverity() {
        return severity;
    }

    public String getUrgency() {
        return urgency;
    }

    public String getAreas() {
        return areas;
    }

    public String getCategory() {
        return category;
    }

    public String getCertainty() {
        return certainty;
    }

    public String getEvent() {
        return event;
    }

    public String getNote() {
        return note;
    }

    public LocalDateTime getEffective() {
        return effective;
    }

    public LocalDateTime getExpires() {
        return expires;
    }

    public String getDesc() {
        return desc;
    }

    public String getInstruction() {
        return instruction;
    }

    
    
}
