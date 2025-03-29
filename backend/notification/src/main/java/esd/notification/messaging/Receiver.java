package esd.notification.messaging;

import java.util.concurrent.CountDownLatch;

import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
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

    @Autowired
    private RabbitTemplate rabbitTemplate;

    private CountDownLatch latch = new CountDownLatch(1);

    private void sendReply(String correlationId, int statusCode) {
        MessageProperties replyProps = new MessageProperties();
        if (correlationId != null) {
            replyProps.setCorrelationId(correlationId);
        }
        Message replyMessage = new Message(
            String.valueOf(statusCode).getBytes(),
            replyProps
        );
        rabbitTemplate.send(
            Messager.topicExchangeName,
            "alert.notification.reply",
            replyMessage
        );
    }

    public void receiveMessage(Message message) {
        MessageProperties props = message.getMessageProperties();
        String correlationId = props.getCorrelationId();
        byte[] body = message.getBody();
        
        // Process the message
        String messageStr = new String(body);
        if (messageStr.isEmpty()) {
            System.out.println("Received empty message, emergency_monitoring test successful");
            sendReply(correlationId, 200);
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
            
            // Send success reply
            sendReply(correlationId, 200);
            
        } catch (JsonProcessingException e) {
            System.err.println("Failed to parse notification: " + e.getMessage());
            sendReply(correlationId, 500);
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("Failed to send notification: " + e.getMessage());
            sendReply(correlationId, 500);
            e.printStackTrace();
        }

        latch.countDown();
    }

    public CountDownLatch getLatch() {
        return latch;
    }
}
