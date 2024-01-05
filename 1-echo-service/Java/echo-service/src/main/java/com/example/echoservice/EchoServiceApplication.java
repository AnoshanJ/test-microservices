package com.example.echoservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpStatus;
import jakarta.servlet.http.HttpServletResponse;


@SpringBootApplication
@RestController
public class EchoServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(EchoServiceApplication.class, args);
	}

	// Health Check endpoint
	@GetMapping("/health")
	public String health(HttpServletResponse response) {
		response.setStatus(HttpStatus.OK.value());
		return "Service Running!";
	}
	// Echo endpoint
	@PostMapping("/echo")
	public String echo(@RequestBody String message , HttpServletResponse response) {
		response.setStatus(HttpStatus.OK.value());
		return message;
	}


}
