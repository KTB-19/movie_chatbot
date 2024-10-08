package com.ktb19.moviechatbot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class MoviechatbotApplication {

	public static void main(String[] args) {
		SpringApplication.run(MoviechatbotApplication.class, args);
	}

}
