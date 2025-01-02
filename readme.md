### Setting up an Opne data cube

1. git clone https://github.com/opendatacube/datacube-core
2. cd datacube-core/index
3. vi docker-compose.yml
4. 추가 및 수정
    ```xml
    name: datacube18 #추가!

    services:
    # Start docker container for PostgreSQL to mock RDS
    postgres:
        hostname: postgres
        image: postgres:15-alpine
        ports:
        - "5434:5432"
        environment:
        POSTGRES_PASSWORD: opendatacubepassword
        # restart: always #주석처리!
        healthcheck:
        test: ["CMD-SHELL", "pg_isready -h postgres -U postgres"]
        interval: 5s
        timeout: 5s
        retries: 5
        volumes: #추가!
        - ./volume/postgresql:/var/lib/postgresql/data:Z #추가!

    # Start docker container for Datacube-Index
    index:
        build: .
        image: datacube-index
        environment:
        - DB_HOSTNAME=host.docker.internal #수정!
        - DB_USERNAME=postgres
        - DB_PASSWORD=opendatacubepassword
        - DB_DATABASE=postgres
        - DB_PORT=5434 #수정!
        - AWS_DEFAULT_REGION=ap-southeast-2
        - PRODUCT_CATALOG=https://raw.githubusercontent.com/GeoscienceAustralia/dea-config/a4f39b485b33608a016032d9987251881fec4b6f/workspaces/sandbox-products.csv
        - METADATA_CATALOG=https://raw.githubusercontent.com/GeoscienceAustralia/dea-config/a4f39b485b33608a016032d9987251881fec4b6f/workspaces/sandbox-metadata.yaml
        depends_on:
        postgres:
            condition: service_healthy

        command: tail -f /dev/null
    ```
5. docker compose up -d

<br><br>
### Database setup
1. docker desktop postgres-1 터미널
   1. su - postgres
   2. createdb datacube
2. docker desktop index-1 터미널
   1. datacube -v system init
3. DB connection 확인
   <br>url : jdbc:postgresql://localhost:5434/postgres
   <br>username : postgres
   <br>password : opendatacubepassword
