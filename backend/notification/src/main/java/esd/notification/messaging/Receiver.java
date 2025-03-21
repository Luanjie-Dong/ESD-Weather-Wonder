package esd.notification.messaging;

import java.util.concurrent.CountDownLatch;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import esd.notification.models.NotificationDAO;
import esd.notification.services.EmailService;

@Component
public class Receiver {
    
    @Autowired
    @Lazy
    private Runner runner;

    @Autowired
    private EmailService emailService;

    private CountDownLatch latch = new CountDownLatch(1);

    public void receiveMessage(String message) {
        System.out.println("Received <" + message + ">");
        latch.countDown();
    }

    public void receiveMessage(byte[] message) {
        // Process the message
        String messageStr = new String(message);
        if (messageStr.isEmpty()) {
            System.out.println("Received empty message");
            latch.countDown();
            return;
        }

        ObjectMapper mapper = new ObjectMapper();
        try {
            NotificationDAO notification = mapper.readValue(messageStr, NotificationDAO.class);
            emailService.sendEmail(
                notification.getRecipients(), 
                notification.getSubject(), 
                notification.getContent(),
                notification.isBcc()
            );
            if (notification.getSubject().equals("Emergency Weather Alert")) {
                runner.run("Alert Email sent");
            }
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        latch.countDown();
    }

    public CountDownLatch getLatch() {
        return latch;
    }
}
