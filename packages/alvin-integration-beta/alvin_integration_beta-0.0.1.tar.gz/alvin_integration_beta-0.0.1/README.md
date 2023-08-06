# Alvin Integration Package

This package contains all the modules related with integrating a Producer such as Airflow with the Alvin platform.

## Running locally

Make sure the Alvin backend API is up and running. 
It should be listening on this address: [http://host.docker.internal:8000](http://host.docker.internal:8000)

Make sure the Alvin UI (the Alvin web dashboard) is up and running.

Create an **Alvin API key** if you don't have one already:

1. Either in the web browser via the Alvin UI
2. Or on the command line with this script: [../../backend/scripts/create-api-key](../../backend/scripts/create-api-key)

Once created it looks like this: `aF2Fb2JifhRRnDjPM4K481bnYhcNi-xlukn8gkBnhjQ=`.

Create an Airflow platform in the Alvin UI:

1. Go to [http://localhost:8080/settings/platforms/create/airflow](http://localhost:8080/settings/platforms/create/airflow)
   You may have to change the TCP port in case that's being used by e.g. Airflow services. 
   Check the UI script output to make sure what port is being used by the Alvin UI.
2. Create the Airflow platform with some lowercase characters e.g. `airflowdev` 
   by filling the fields **Name** and **Display Name**.
   The Alvin Platform Name is also known as Platform ID.
3. You can check the details later via SQL on the database with:
   ```sql
   select * 
   from monda_data.data_platform dp 
   where dp.id = 'airflowdev';
   ```

Make sure you amend the docker-compose YAML files with these details:

```yaml
AIRFLOW__LINEAGE__BACKEND: alvin_integration.producers.airflow.lineage.backend.AlvinAirflowLineageBackend
ALVIN_URL: 'http://host.docker.internal:8000'
ALVIN_API_KEY: 'aF2Fb2JifhRRnDjPM4K481bnYhcNi-xlukn8gkBnhjQ='
ALVIN_PLATFORM_ID: 'airflowdev'
```

### Build Docker Images

Execute the following command for Airflow 2:

```make build-airflow```

Execute the following command for Airflow 1:

```make build-legacy```

### Running Airflow

Execute the following command for Airflow 2:

```make run-airflow```

Execute the following command for Airflow 1:

```make run-legacy```

See the bootstrap troubleshooting details about the Docker Service `airflow-init`
further below in this doc. 

At the first time running this you need to uncomment the content for this Docker Service.
The next times you may want to comment out most of that code block in that Docker Service.

If the Alvin backend API is not on reach of the Airflow workers, 
then you can troubleshoot this with the following commands.

```sh
# login to the docker container
docker exec -it airflow-airflow-worker-1 /bin/sh
# check the TCP layer
nc -w 1000 -v host.docker.internal 8000
# check the HTTP layer: response status and response headers
curl --connect-timeout 1 -o - -I http://host.docker.internal:8000
# check the HTTP layer: response status and response body
curl --connect-timeout 1 -s -w "\nresponse code: %{http_code}\n" http://host.docker.internal:8000
```

You should make sure the TCP layer is on reach and the HTTP layer works as expected.

The Alvin backend API is a Python application running as a Uvicorn web server managing FastAPI endpoints.

Bear in mind that the docker-compose services are not sharing the network host with your laptop.
Depending on the kernel (Linux or Darwin), the architecture (x86_64 - Intel/AMD or arm64 - Apple M1)
and the version of your Docker installation you may have to troubleshoot further.

The `host.docker.internal` detail allows to link your laptop host to the Docker network.
This may or may not work depending on your circumstances e.g. the Docker version, 
see here for further details [https://docs.docker.com/desktop/mac/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host](https://docs.docker.com/desktop/mac/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host).

### End to end testing 

There are a couple of things to bear in mind:

1. As an alternative to the Alvin backend API, there is a dummy API that runs as a docker service.
   It just prints all the HTTP requests from Airflow without validating the Alvin API key.
   The Docker Service is defined as `alvin_backend` in the YAML script (far bottom):
   the Alvin URL should be provided as `ALVIN_URL: 'http://alvin_backend:9000'`
2. The Docker Service `airflow-init` deals with the initialization setup e.g. the Database details.
   The Docker Service is the first to start and all the other services inherit from it once it's done running.
   Sometimes depending on the logs (and errors) you see for `airflow-init` you may have to
   comment/uncomment the YAML part related to the init service between these 
   check marks `# yamllint disable rule:line-length` and `# yamllint enable rule:line-length`.
3. The Airflow UI (the Docker Service `airflow-airflow-webserver-1`) listens on [http://localhost:8080](http://localhost:8080)
   The Airflow UI credentials are: `airflow` and `airflow`.