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
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <h2 style="color: #e74c3c; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px;">
                            ⚠️ %s: %s
                        </h2>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            <strong>Event:</strong> %s
                        </p>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            <strong>This is an ongoing weather alert effective from %s to %s.</strong>
                        </p>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            <strong>Severity:</strong> %s<br>
                            <strong>Urgency:</strong> %s<br>
                            <strong>Certainty:</strong> %s
                        </p>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            <strong>Areas Affected:</strong>
                        </p>
                        <ul style="font-size: 16px; margin-bottom: 10px; padding-left: 20px;">
                            %s
                        </ul>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            %s
                        </p>
                        <p style="font-size: 16px; margin-bottom: 10px;">
                            %s
                        </p>
                        <p style="font-size: 14px; color: #777; margin-top: 30px;">
                            🛡️ Stay safe and take necessary precautions.
                        </p>
                    </div>
                </body>
            </html>
            """.formatted(
                msgType != null ? msgType : "Alert",
                headline,
                event,
                effective.format(DateTimeFormatter.ofPattern("MMMM dd, yyyy 'at' hh:mm a")),
                expires.format(DateTimeFormatter.ofPattern("MMMM dd, yyyy 'at' hh:mm a")),
                severity,
                urgency,
                certainty,
                formatAreas(areas),
                desc != null ? desc : "",
                instruction != null ? instruction : "There is no guidance for this weather emergency. Please remain vigilant and follow local news for updates."
            );
    }

    private String formatAreas(String areas) {
        StringBuilder formattedAreas = new StringBuilder();
        for (String area : areas.split("; ")) {
            formattedAreas.append("<li>📍 ").append(area).append("</li>");
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