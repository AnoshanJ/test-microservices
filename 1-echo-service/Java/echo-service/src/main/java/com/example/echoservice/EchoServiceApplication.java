package com.example.echoservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;


@SpringBootApplication
public class EchoServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(EchoServiceApplication.class, args);
	}

	@GetMapping("/health")
	public String health() {
		return "Service Running!";
	}


}
