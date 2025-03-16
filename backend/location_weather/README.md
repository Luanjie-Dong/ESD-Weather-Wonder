## Quick Setup 
Note: MS is running on 5003

### Local Deployment
#### Running the project directly
1. Create your own supabase table and schema, then update your `.env` file with your credentials
```bash
SUPABASE_URL = YOUR_SUPABASE_DB_URL
SUPABASE_KEY = YOUR_SUPABASE_API_KEY
```
2. Requirements 
```bash
pip install -r requirements.txt
```
3. Run
```bash
python main.py
```


#### Building docker image
1. Docker Build
```bash
docker build -t location_weather .
```
2. Docker Run
```bash
docker run -p 5003:5003 --env-file .env location_weather
```

#### Auth
1. Generate JWT Secret with OpenSSL
```bash
openssl random -base64 256
```
2. Update `.env` file with JWT Secret
```bash
JWT_SECRET = YOUR_JWT_SECRET
```
3. Share your JWT Secret with the other services that depend on you and call them
4. Remember to also add in your service URL, then use this in your code to call the desired MS to make it dynamic
```bash
MICROSERVICE_URL = SERVICES_WHO_WILL_CALL_YOUR_MS_URL
```