package esd.emergencyweather;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MainController {

    @Autowired
    private MainService mainService;

    // Endpoints to override cron job for function testing
    @GetMapping("/check-alerts")
    public ResponseEntity checkAlerts() {
        try {
            mainService.checkAlerts();
            return ResponseEntity.ok("Alerts checked successfully.");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("Error checking alerts: " + e.getMessage());
        }
    }
}
