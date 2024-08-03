package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ktb19.moviechatbot.dto.QueriesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.exception.FailParsingPyObjectToJsonException;
import com.ktb19.moviechatbot.exception.PyFunctionNotFoundException;
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
    public QueryDto parse(String message) {

        PyFunction parseQuery = getPythonFunction("src/main/java/com/ktb19/moviechatbot/ai/test1.py", "parseQuery");
        PyObject jsonPyObject = parseQuery.__call__(new PyUnicode(message));

        QueryDto dto = toQueryDto(jsonPyObject);

        return dto;
    }

    public QueryDto parseAdditional(QueryDto parsedQuery, QueriesDto additionQueries) {

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
        PyFunction pyFunction = interpreter.get(functionName, PyFunction.class);

        if (pyFunction == null) {
            throw new PyFunctionNotFoundException(functionName);
        }

        return pyFunction;
    }

    private QueryDto union(QueryDto parsedQuery, QueryDto dto) {

        QueryDto result = new QueryDto();

        result.setMovieName(parsedQuery.getMovieName() != null ? parsedQuery.getMovieName() : dto.getMovieName());
        result.setRegion(parsedQuery.getRegion() != null ? parsedQuery.getRegion() : dto.getRegion());
        result.setDate(parsedQuery.getDate() != null ? parsedQuery.getDate() : dto.getDate());

        return result;
    }

    private QueryDto toQueryDto(PyObject pyObject) {

        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());

        try {
            QueryDto dto = mapper.readValue(pyObject.toString(), QueryDto.class);

            log.info("dto.getMovieName() : " + dto.getMovieName());
            log.info("dto.getRegion() : " + dto.getRegion());
            log.info("dto.getDate() : " + dto.getDate());

            return dto;

        } catch (JsonProcessingException e) {
            throw new FailParsingPyObjectToJsonException(pyObject.toString());
        }
    }
}
