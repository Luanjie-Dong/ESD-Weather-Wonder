package esd.emergencyweather;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import esd.emergencyweather.models.*;

@RestController
public class MainController {

    @Autowired
    private MainService mainService;

    // Endpoints to override cron job for function testing
    @GetMapping("/check-alerts")
    public void checkAlerts() {
        mainService.checkAlerts();
    }
}
