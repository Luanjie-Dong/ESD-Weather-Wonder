package esd.emergencyweather;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.datatype.jsr310.JSR310Module;

import esd.emergencyweather.models.*;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;

@Service
public class MainWrapper {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${notification.ms.url}")
    private String notificationMSUrl;

    @Value("${user.ms.url}")
    private String userMSUrl;

    @Value("${weather.wrapper.url}")
    private String weatherWrapperUrl;
    
    public EmailGroupbyLocation[] getEmailsByLocation() {
        URI uri = UriComponentsBuilder.fromHttpUrl(userMSUrl + "/emails-by-location").build().toUri();
        EmailsByLocationDAO emailsByLocationDAO = restTemplate.getForObject(uri, EmailsByLocationDAO.class);
        return emailsByLocationDAO.getEmails_by_location();
    }

    public Alert[] getAlertsByLocation(String country, String state, String city) {
        
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JSR310Module());

        // Construct the GraphQL query
        String query = """
            query {
                getAlerts(country: "%s", state: "%s", city: "%s") {
                    alerts {
                        alert {
                            headline,
                            msgType,
                            severity,
                            urgency,
                            areas,
                            category,
                            certainty,
                            event,
                            note,
                            effective,
                            expires,
                            desc,
                            instruction
                        }
                    }
                }
            }
        """.formatted(country, state, city);
        try {
            // Create a POST request with the query in the body
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> requestBodyMap = new HashMap<>();
            requestBodyMap.put("query", query);
            String requestBody = mapper.writeValueAsString(requestBodyMap);
            HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);

            // Send the POST request
            RestTemplate restTemplate = new RestTemplate();
            String endpoint = weatherWrapperUrl + "/graphql";
            String responseJson = restTemplate.postForObject(endpoint, entity, String.class);

            // Deserialize the response into an array of Alert objects
            JsonNode responseNode = mapper.readTree(responseJson);
            JsonNode alertsNode = responseNode.get("data").get("getAlerts").get("alerts").get("alert");
            Alert[] alerts = mapper.convertValue(alertsNode, Alert[].class);
            return alerts;
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return new Alert[0];
        }
    }
}
