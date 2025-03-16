package esd.emergencyweather;

import org.springframework.scheduling.annotation.Scheduled;

import java.time.LocalDateTime;

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
        for (EmailGroupbyLocation emailsByLocation : emailsByLocations) {
            System.out.println("Getting alerts for " + emailsByLocation.getCountry() + ", " + emailsByLocation.getState() + ", " + emailsByLocation.getCity());
            Alert[] alerts = mainWrapper.getAlertsByLocation(emailsByLocation.getCountry(), emailsByLocation.getState(), emailsByLocation.getCity());
            if (alerts.length > 0) {
                for (Alert alert : alerts) {
                    if (alert.getEffective().isAfter(outdatedTime)) {
                        // System.out.println(alert);
                    } 
                    System.out.println(alert);
                }
            } else {
                System.out.println("No alerts found for " + emailsByLocation.getCountry() + ", " + emailsByLocation.getState() + ", " + emailsByLocation.getCity());
            }
        }
    }
    
}
