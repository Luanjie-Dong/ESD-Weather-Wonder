Note::
This MS uses the Supabase service key

Docker Commands::
docker build -t weatherwonder:user ./
docker run --env-file .env -p 5001:5001 weatherwonder:user