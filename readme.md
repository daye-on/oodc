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
   - su - postgres
   - createdb datacube
2. docker desktop index-1 터미널
   - datacube -v system init
3. DB connection 확인
   <br>url : jdbc:postgresql://localhost:5434/postgres
   <br>username : postgres
   <br>password : opendatacubepassword

<br><br>
### Configuring the ODC Database
1. [Metadata Types](https://explorer.dea.ga.gov.au/metadata-types)
   <br>v1.9에서 지원하는 metadata types은 eo3
-  eo3
-  eo3_intertidal
-  eo3_landsat_ard
-  eo3_sentinel_ard
1. metadata type yaml 파일 다운로드
   <br> 하단 Definition View Raw &rightarrow; 다른 이름으로 저장
2. docker desktop index-1 View files
   <br> 다운로드 받은 metadata yaml 파일 drag & drop
3. docker desktop index-1 터미널
   - datacube metadata add 다운받은파일
4. [1] 의 metadata type에 해당하는 product 선택 [예시](https://explorer.dea.ga.gov.au/products/ga_ls9c_ard_3)
5. product yaml 파일 다운로드
   <br> 하단 Definition View Raw &rightarrow; 다른 이름으로 저장
6. [3] 과정 반복
7. docker desktop index-1 터미널
   - datacube product add 다운받은파일
8. [5] 의 product에 해당하는 dataset 선택 [예시](https://explorer.dea.ga.gov.au/products/ga_ls9c_ard_3/datasets/bb3b9c93-0238-448f-83ee-a8df86207631)
9.  dataset yaml 파일 다운로드
   <br> 하단 Definition View Raw &rightarrow; 다른 이름으로 저장
10. [3] 과정 반복
11. docker desktop index-1 터미널
    - datacube dataset add 다운받은파일


<br><br>
Ref: [Open Data Cube](https://datacube-core.readthedocs.io/en/stable/installation/index.html)<br>
Ref: [Digital Earth Australia](https://explorer.dea.ga.gov.au/products)