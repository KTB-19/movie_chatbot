package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ktb19.moviechatbot.dto.QueriesDto;
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

    public QueryDto parseAdditional(String message) {

        try {

            PythonInterpreter.initialize(null, null, new String[]{message});
            PythonInterpreter interpreter = new PythonInterpreter();
            interpreter.execfile("src/main/java/com/ktb19/moviechatbot/ai/test1.py");

            PyObject json = interpreter.get("result", PyObject.class);

            QueryDto dto = toQueryDto(json);

            return dto;
        } catch (Exception e) {
            log.error(e.getMessage());
        }

        return new QueryDto();
    }

    public QueryDto parseAdditional(QueryDto parsedQuery, QueriesDto additionQueries) {

        //addtionQueries를 python 파일에 보내서, 응답 받기

        //응답을 QueryDto로 mapping

        //QueryDto 중 빈칸을 parsedQuery에서 가져와서 합치기

            PythonInterpreter.initialize(null, null, getInputs(additionQueries));
            PythonInterpreter interpreter = new PythonInterpreter();

            interpreter.execfile("src/main/java/com/ktb19/moviechatbot/ai/test2.py");

            PyObject json = interpreter.get("result", PyObject.class);

        try {

            QueryDto dto = toQueryDto(json);

            return dto;
        } catch (Exception e) {
            log.error(e.getMessage());
        }

        return new QueryDto();
    }

    private static QueryDto toQueryDto(PyObject json) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        QueryDto dto = mapper.readValue(json.toString(), QueryDto.class);
        log.info("dto.getMovieName() : " + dto.getMovieName());
        log.info("dto.getRegion() : " + dto.getRegion());
        log.info("dto.getDate() : " + dto.getDate());
        return dto;
    }

    private static String[] getInputs(QueriesDto additionQueries) {
        return new String[]{additionQueries.getMovieNameQuery(), additionQueries.getRegionQuery(), additionQueries.getDateQuery()};
    }
}
