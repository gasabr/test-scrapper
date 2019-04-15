# hh.ru scrapper

#### Requirements:
- docker-compose compatible with the 3rd file version

#### How to use it:
1. start all the services
    ```bash
    docker-compose up -d
    ```
2. wait for 10-15 seconds AFTER all containers are up, while migrations are done.
3. now everything is up and running on `http://localhost:8000`and you can use API

#### API
* `http://localhost:8000/app/search` -- does the work of searching and parsing vacancies.
* `http://localhost:8000/app/status` -- displays amount of active workers doing the 1st task
* `http://localhost:8000/app/list` -- shows the listed of parsed vacancies
* `http://localhost:8000/app/links` -- shows the links to parsed vacancies

Everything is text-based and was meant to be used in terminal, for example, to check if all vacancies are there, run:
```bash
$ curl localhost:8000/app/list | wc -l
```

#### Notes:
* there is sleep(2) in one of the workers, just to be able to see the `status`.
* have not disabled DEBUG, but don't think that's a big deal for small task like this.
* was not able to log inside Celery tasks, but all the endpoints log straight to `docker-compose log`