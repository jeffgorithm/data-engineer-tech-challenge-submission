docker run \
--rm \
-p 5432:5432 \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_USER=postgres \
--name test_preloaded_db \
preloaded_db:latest