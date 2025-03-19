package esd.notification.messaging;

import java.util.concurrent.CountDownLatch;
import org.springframework.stereotype.Component;

@Component
public class Receiver {
    
    private CountDownLatch latch = new CountDownLatch(1);

    public void receiveMessage(String message) {
        System.out.println("Notification MS received <" + message + ">");
        latch.countDown();
    }

    public void receiveMessage(byte[] message) {
        // Process the message
        String messageStr = new String(message);
        System.out.println("Received message: " + messageStr);
    }

    public CountDownLatch getLatch() {
        return latch;
    }
}
