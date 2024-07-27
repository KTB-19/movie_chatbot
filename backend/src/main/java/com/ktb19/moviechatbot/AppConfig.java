package com.ktb19.moviechatbot;

import org.python.util.PythonInterpreter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean
    public PythonInterpreter pythonInterpreter() {
        PythonInterpreter.initialize(null, null, new String[0]);
        return new PythonInterpreter();
    }
}
