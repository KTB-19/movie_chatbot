package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ktb19.moviechatbot.dto.QueryDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class ParseService {

    public QueryDto parse(String query) {

        try {

            PythonInterpreter.initialize(null, null, new String[]{query});
            PythonInterpreter interpreter = new PythonInterpreter();
            interpreter.execfile("src/main/java/com/ktb19/moviechatbot/ai/test.py");

            PyObject json = interpreter.get("result", PyObject.class);

            ObjectMapper mapper = new ObjectMapper();
            QueryDto dto = mapper.readValue(json.toString(), QueryDto.class);
            log.info("dto.getMovieName() : " + dto.getMovieName());
            log.info("dto.getRegion() : " + dto.getRegion());
            log.info("dto.getDate() : " + dto.getDate());

            return dto;
        } catch (Exception e) {
            log.error(e.getMessage());
        }

        return null;
    }
}
