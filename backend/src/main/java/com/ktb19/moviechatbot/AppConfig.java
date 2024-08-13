package com.ktb19.moviechatbot;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.python.util.PythonInterpreter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean
    public PythonInterpreter pythonInterpreter() {
        System.setProperty("python.import.site", "false");
        PythonInterpreter.initialize(null, null, new String[0]);
        PythonInterpreter python = new PythonInterpreter();

        StringBuilder script1 = new StringBuilder();
        script1.append("import ensurepip\n");
        script1.append("ensurepip._main()");
        python.exec(script1.toString());

        StringBuilder script2 = new StringBuilder();
//        script2.append("import pip\n");
//        script2.append("pip.main(['install', 'openai'])");
        script2.append("import sys\n");
        script2.append("import subprocess\n");
        script2.append("subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openai'])");
        python.exec(script2.toString());

        return python;
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());

        return mapper;
    }
}
