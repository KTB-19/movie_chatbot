package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ktb19.moviechatbot.dto.QueriesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyUnicode;
import org.python.util.PythonInterpreter;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class ParseService {

    private final PythonInterpreter interpreter;
    public QueryDto parse(String message) throws JsonProcessingException {

        PyFunction parseQuery = getPythonFunction("src/main/java/com/ktb19/moviechatbot/ai/test1.py", "parseQuery");
        PyObject json = parseQuery.__call__(new PyUnicode(message));

        QueryDto dto = toQueryDto(json);

        return dto;
    }

    public QueryDto parseAdditional(QueryDto parsedQuery, QueriesDto additionQueries) throws JsonProcessingException {

        PyFunction parseQueries = getPythonFunction("src/main/java/com/ktb19/moviechatbot/ai/test2.py", "parseQueries");
        PyObject json = parseQueries.__call__(
                new PyUnicode(additionQueries.getMovieNameQuery()),
                new PyUnicode(additionQueries.getRegionQuery()),
                new PyUnicode(additionQueries.getDateQuery())
        );

        QueryDto dto = toQueryDto(json);

        return union(parsedQuery, dto);
    }

    private PyFunction getPythonFunction(String scriptPath, String functionName) {

        interpreter.execfile(scriptPath);

        return interpreter.get(functionName, PyFunction.class);
    }

    private QueryDto union(QueryDto parsedQuery, QueryDto dto) {

        QueryDto result = new QueryDto();

        result.setMovieName(parsedQuery.getMovieName() != null ? parsedQuery.getMovieName() : dto.getMovieName());
        result.setRegion(parsedQuery.getRegion() != null ? parsedQuery.getRegion() : dto.getRegion());
        result.setDate(parsedQuery.getDate() != null ? parsedQuery.getDate() : dto.getDate());

        return result;
    }

    private QueryDto toQueryDto(PyObject json) throws JsonProcessingException {

        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        QueryDto dto = mapper.readValue(json.toString(), QueryDto.class);
        log.info("dto.getMovieName() : " + dto.getMovieName());
        log.info("dto.getRegion() : " + dto.getRegion());
        log.info("dto.getDate() : " + dto.getDate());
        return dto;
    }
}
