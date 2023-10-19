# bewiseai-test

To start the service use the command:
    `docker compose up --build`
It will lead to a few failures on start but when the database will setup
the service will start the work.

After this in different terminal you can check the queries with the command:
	`curl -X POST http://localhost:3000/questions -H 'Content-Type: application/json' -d '{"questions_num": 5}'`
