package esd.emergencyweather;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.scheduling.annotation.Async;
import java.time.LocalDateTime;
import java.util.concurrent.CompletableFuture;
import java.util.ArrayList;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import esd.emergencyweather.models.*;

@Service
public class MainService {
    
    @Autowired
    private MainWrapper mainWrapper;

    @Scheduled(cron = "0 0/30 * * * *", zone = "UTC")
    public void checkAlerts() {
        LocalDateTime triggerTime = LocalDateTime.now();
        LocalDateTime outdatedTime = triggerTime.minusMinutes(30);

        EmailGroupbyLocation[] emailsByLocations = mainWrapper.getEmailsByLocation();
        List<CompletableFuture<Void>> futures = new ArrayList<>();

        for (EmailGroupbyLocation emailsByLocation : emailsByLocations) {
            CompletableFuture<Void> future = processLocationAlerts(emailsByLocation, outdatedTime);
            futures.add(future);
        }

        // Wait for all async tasks to complete
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
    }

    @Async("alertTaskExecutor")
    private CompletableFuture<Void> processLocationAlerts(EmailGroupbyLocation emailsByLocation, LocalDateTime outdatedTime) {
        System.out.println("Getting alerts for " + emailsByLocation.getCountry() + ", " + 
            emailsByLocation.getState() + ", " + emailsByLocation.getCity());
        
        Alert[] alerts = mainWrapper.getAlertsByLocation(
            emailsByLocation.getCountry(), 
            emailsByLocation.getState(), 
            emailsByLocation.getCity()
        );

        if (alerts.length > 0) {
            for (Alert alert : alerts) {
                // Comment this out for testing
                if (alert.getEffective().isAfter(outdatedTime)) {
                    mainWrapper.sendEmails(emailsByLocation.getEmails(), alert);
                }
                // Uncomment this for testing
                // mainWrapper.sendEmails(emailsByLocation.getEmails(), alert);
            }
            System.out.println("Finished sending latest alerts for " + emailsByLocation.getCountry() + 
                ", " + emailsByLocation.getState() + ", " + emailsByLocation.getCity());
        } else {
            System.out.println("No alerts found for " + emailsByLocation.getCountry() + 
                ", " + emailsByLocation.getState() + ", " + emailsByLocation.getCity());
        }

        return CompletableFuture.completedFuture(null);
    }
}
