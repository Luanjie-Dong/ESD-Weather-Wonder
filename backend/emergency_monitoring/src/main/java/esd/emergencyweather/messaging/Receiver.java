package esd.emergencyweather.messaging;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.springframework.stereotype.Component;
import org.springframework.amqp.core.Message;

@Component
public class Receiver {
    private final ConcurrentHashMap<String, ReplyStatus> correlationStatus = new ConcurrentHashMap<>();

    public void receiveMessage(Message message) {
        String correlationId = message.getMessageProperties().getCorrelationId();
        String statusStr = new String(message.getBody());
        int statusCode;
        
        try {
            statusCode = Integer.parseInt(statusStr);
        } catch (NumberFormatException e) {
            statusCode = 500;
        }

        System.out.println("Received reply for correlation ID " + correlationId + ": " + statusCode);
        
        ReplyStatus status = correlationStatus.get(correlationId);
        if (status != null) {
            status.setStatusCode(statusCode);
            status.getLatch().countDown();
        }
    }

    public boolean waitForReply(String correlationId, long timeout) {
        ReplyStatus status = new ReplyStatus();
        correlationStatus.put(correlationId, status);
        
        try {
            boolean received = status.getLatch().await(timeout, TimeUnit.MILLISECONDS);
            if (received) {
                return status.getStatusCode() == 200;
            }
            return false;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        } finally {
            correlationStatus.remove(correlationId);
        }
    }

    private static class ReplyStatus {
        private final CountDownLatch latch = new CountDownLatch(1);
        private int statusCode = 500;

        public CountDownLatch getLatch() {
            return latch;
        }

        public void setStatusCode(int code) {
            this.statusCode = code;
        }

        public int getStatusCode() {
            return statusCode;
        }
    }
}
