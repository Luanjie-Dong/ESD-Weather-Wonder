package esd.emergencyweather.messaging;

import java.util.concurrent.TimeUnit;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class Runner implements CommandLineRunner {
    private final RabbitTemplate rabbitTemplate;
    private final Receiver receiver;

    public Runner(Receiver receiver, RabbitTemplate rabbitTemplate) {
        this.receiver = receiver;
        this.rabbitTemplate = rabbitTemplate;
    }

    @Override
    public void run(String... args) throws Exception {
        // System.out.println("Sending message...");
        String message = String.join(",", args);
        MessageProperties messageProperties = new MessageProperties();
        messageProperties.setPriority(10);
        Message rabbitMessage = new Message(message.getBytes(), messageProperties);
        rabbitTemplate.convertAndSend(Messager.topicExchangeName, "weather.alert.notification", rabbitMessage);
        receiver.getLatch().await(10000, TimeUnit.MILLISECONDS);
    }
}
