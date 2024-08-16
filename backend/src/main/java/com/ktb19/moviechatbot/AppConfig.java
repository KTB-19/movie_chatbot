package com.ktb19.moviechatbot;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

//    @Bean
//    public PythonInterpreter pythonInterpreter() {
//        PythonInterpreter.initialize(null, null, new String[0]);
//        return new PythonInterpreter();
//    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());

        return mapper;
    }
}
