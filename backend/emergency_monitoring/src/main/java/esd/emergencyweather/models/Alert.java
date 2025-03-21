package esd.emergencyweather.models;

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

    public Alert() {
    }

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

    public String toEmailString() {
        return """
            <html>
                <body>
                    <h2>%s: %s</h2>
                    <p>This is an ongoing %s alert effective from %s till %s for the following areas:</p>
                    <ul>
                        %s
                    </ul>
                    <p>%s</p>
                </body>
            </html>
        """.formatted(
            msgType != null ? msgType : "Alert",
            headline,
            event,
            effective.format(DateTimeFormatter.ofPattern("MMMM dd, yyyy 'at' hh:mm a")),
            expires.format(DateTimeFormatter.ofPattern("MMMM dd, yyyy 'at' hh:mm a")),
            formatAreas(areas),
            instruction
        );
    }

    private String formatAreas(String areas) {
        StringBuilder formattedAreas = new StringBuilder();
        for (String area : areas.split("; ")) {
            formattedAreas.append("<li>").append(area).append("</li>");
        }
        return formattedAreas.toString();
    }

    public String toString() {
        return """
            %s: %s
            Effective %s till %s
        """.formatted(msgType, headline, effective, expires);
    }
}