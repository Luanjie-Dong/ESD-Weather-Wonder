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