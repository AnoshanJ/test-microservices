# Echo Service Using Java-SpringBoot

## Use case

When the service is invoked with a message, the service will respond with the same message received via an HTTP POST.

## How to Run

`mvn clean compile package
`
`java -jar ./target/echo-service-0.0.1-SNAPSHOT.jar`

## Build the project

`./mvnw clean install`
Run the service

`./mvnw spring-boot:run`

## Test the endpoint

```
curl -L 'http://localhost:8080/echo' -H 'Content-Type: text/plain' -d '"Hello Word!"'
```

```
curl -L 'http://localhost:8080/health'
```
