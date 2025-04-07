# Weather Wonder
![Alt text](./readme_images/esd_weatherwonder_frontend.jpg)
Weather Wonder is a microservices-based application that provides weather forecasts, emergency monitoring, and notifications. It includes a backend with multiple microservices, an API gateway, and a frontend built with Next.js.

## Project Structure
```
ESD-Weather-Wonder
├── backend/ # Backend microservices 
├── api_gateway/ # API Gateway configuration 
├── frontend/ # Frontend application 
├── run.sh # Script to start all services (Linux/Mac) 
├── run.bat # Script to start all services (Windows) 
├── down.sh # Script to stop all services (Linux/Mac) 
├── down.bat # Script to stop all services (Windows) 
├── .gitignore # Git ignore file 
├── package.json # Project dependencies 
├── package-lock.json # Dependency lock file 
└── README.md # Project documentation
```

## Prerequisites

- Docker and Docker Compose
- Node.js (v16 or later)
- npm or yarn

## Setting Up the Project

### 1. Clone the Repository
```
bash
git clone https://github.com/your-username/ESD-Weather-Wonder.git
cd ESD-Weather-Wonder
```

### 2. Install frontend dependencies
```
cd frontend
npm install
cd ../
```

### 3. Configure environment variables
The project requires several .env files for different services. 
Below are the required .env files and their configurations:
* For instructor use: Please refer to the secrets.txt file attached with the project submission for the environment variables.

#### Backend Microservices
Notification Service (backend/notification/src/main/resources/.env):
```
EMAIL_USERNAME=your_email_username
EMAIL_PASSWORD=your_email_password
RABBITMQ_HOST=rabbitmq
```
* To run this locally, make sure to use a private Gmail account not tagged to any institution/organization
* Use an _app password_ to authorize actions on your Gmail account. You can find a guide to generating your app password here:
https://help.prowly.com/how-to-create-use-gmail-app-passwords
---
Weather Wrapper Service (backend/weather/src/main/resources/.env):
```
WEATHERAPI_KEY=your_weather_api_key
```
---
Emergency Monitoring Service (backend/emergency_monitoring/src/main/resources/.env):
```
WEATHER_WRAPPER_URL="http://weather:8081"
NOTIFICATION_MS_URL="http://notification:8083"
USER_MS_URL="http://user:5001"
RABBITMQ_HOST="rabbitmq"
```
---
User Service (backend/user/.env):
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SUPER_KEY=your_supabase_service_role_key
AMQP_HOST=rabbitmq
AMQP_PORT=5672
AMQP_USER=myuser
AMQP_PASS=secret
EXCHANGE_NAME=esd-weatherwonder
```
---
Location Service (backend/location/.env):
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```
---
Location Weather Service (backend/location_weather/.env):
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
LOCATION_SERVICE_URL=http://location:5002
WEATHER_API_KEY=your_weather_api_key
AMQP_HOST=rabbitmq
AMQP_PORT=5672
AMQP_USER=myuser
AMQP_PASS=secret
EXCHANGE_NAME=esd-weatherwonder
EXCHANGE_TYPE=topic
```
---
Add A Location Service (backend/add_a_location/.env):
```
geocoding_URL = "http://geocoding:5004/encode"
location_URL = "http://location:5002/locations"
poll_weather_URL = "http://poll_weather_forecast:5005/poll-location"
userlocation_URL = "your_outsystems_personal_environment/UserLocation/rest/v1/CreateUserLocation"
```
---
Geocoding Service (backend/geocoding/.env):
```
GEOCODING_API_KEY=your_opencagemap_api_key
```
---
Notify Weather Forecast Service (backend/notify_weather_forecast/.env):
```
AMQP_HOST=rabbitmq
AMQP_PORT=5672
AMQP_USER=myuser
AMQP_PASS=secret
EXCHANGE_NAME=esd-weatherwonder
USER_URL=http://user:5001
USERLOCATION_URL=your_outsystems_personal_environment
```
---
Poll Weather Forecast Service (backend/poll_weather_forecast/.env):
```
LOCATION_URL=http://location:5002
WEATHER_URL=http://weather:8081
LOCATION_WEATHER_URL=http://location_weather:5003
```
---
RabbitMQ Service (backend/rabbitmq/.env):
```
AMQP_HOST = localhost
AMQP_PORT = 5672
EXCHANGE_NAME = esd-weatherwonder
EXCHANGE_TYPE = topic
AMQP_USER = myuser
AMQP_PASS = secret
```

#### API Gateway
API Gateway (api_gateway/.env):
```
POSTGRES_DB=kong
POSTGRES_USER=kong
POSTGRES_PASSWORD=weatherwonderpassword
KONG_DATABASE=postgres
KONG_PG_HOST=kong-database
KONG_PG_USER=kong
KONG_PG_PASSWORD=weatherwonderpassword
KONG_PROXY_ACCESS_LOG=/dev/stdout
KONG_ADMIN_ACCESS_LOG=/dev/stdout
KONG_PROXY_ERROR_LOG=/dev/stderr
KONG_ADMIN_ERROR_LOG=/dev/stderr
KONG_ADMIN_LISTEN=0.0.0.0:8001
KONG_ADMIN_GUI_URL=http://localhost:8002
```

#### Frontend
Frontend (frontend/.env):
```
NEXT_PUBLIC_API_KEY_NAME=weatherwonderapi_key
NEXT_PUBLIC_API_KEY_VALUE=abc123xyz
```

### 4. Start the services
For Linux/Mac Users
```
# To start the services:
run.sh

# To stop the services:
down.sh
```
For Windows Users
```
# To start the services:
run.bat

# To stop the services:
down.bat
```