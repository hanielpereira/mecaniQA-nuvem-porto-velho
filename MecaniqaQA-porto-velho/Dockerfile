FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY target/*.jar /app/api.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "api.jar"]
