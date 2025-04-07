package esd.emergencyweather.messaging;

import java.util.concurrent.TimeUnit;
import java.util.UUID;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class Runner implements CommandLineRunner {
    private final RabbitTemplate rabbitTemplate;
    private final Receiver receiver;
    private static final long REPLY_TIMEOUT = 60000; // 1 minute in milliseconds

    public Runner(Receiver receiver, RabbitTemplate rabbitTemplate) {
        this.receiver = receiver;
        this.rabbitTemplate = rabbitTemplate;
    }

    @Override
    public void run(String... args) throws Exception {
        String message = String.join(",", args);
        sendMessageWithRetry(message);
    }

    private void sendMessageWithRetry(String message) {
        MessageProperties messageProperties = new MessageProperties();
        messageProperties.setPriority(10);
        String correlationId = UUID.randomUUID().toString();
        messageProperties.setCorrelationId(correlationId);
        messageProperties.setReplyTo(Messager.replyQueueName);
        
        Message rabbitMessage = new Message(message.getBytes(), messageProperties);
        
        boolean messageAcknowledged = false;
        int attempts = 1;
        
        while (!messageAcknowledged) {
            System.out.println("Attempt " + attempts + ": Sending message with correlation ID: " + correlationId);
            rabbitTemplate.convertAndSend(Messager.topicExchangeName, "weather.alert.notification", rabbitMessage);
            
            // Wait for reply
            messageAcknowledged = receiver.waitForReply(correlationId, REPLY_TIMEOUT);
            
            if (!messageAcknowledged) {
                System.out.println("Attempt " + attempts + " failed: No successful reply received within timeout, republishing message...");
                attempts++;
            } else {
                System.out.println("Message successfully processed after " + attempts + " attempt(s)");
            }
        }
    }
}
