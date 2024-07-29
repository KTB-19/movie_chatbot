package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ktb19.moviechatbot.dto.QueriesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyUnicode;
import org.python.util.PythonInterpreter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.BDDMockito.*;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.mock;

@SpringBootTest
class ParseServiceTest {

    @Mock
    private PythonInterpreter pythonInterpreter;

    @InjectMocks
    private ParseService parseService;

    @Test
    @DisplayName("주어진 메시지를 파싱하여 QueryDto 객체로 반환한다.")
    void testParse() throws JsonProcessingException {
        // Given
        String message = "test message";
        String jsonString = "{\"movieName\": \"Test Movie\", \"region\": \"Test Region\", \"date\": \"2024-01-01\"}";

        PyFunction mockFunction = mock(PyFunction.class);
        PyObject mockPyObject = new PyUnicode(jsonString);

        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(mockFunction);
        given(mockFunction.__call__(any(PyObject.class))).willReturn(mockPyObject);
        willDoNothing().given(pythonInterpreter).execfile("src/main/java/com/ktb19/moviechatbot/ai/test1.py");

        // When
        QueryDto result = parseService.parse(message);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getMovieName()).isEqualTo("Test Movie");
        assertThat(result.getRegion()).isEqualTo("Test Region");
        assertThat(result.getDate()).isEqualTo("2024-01-01T09:00:00.000");
    }

    @Test
    @DisplayName("추가 쿼리를 파싱하여 기존 parsedQuery와 병합된 QueryDto 객체로 반환한다.")
    void testParseAdditional() throws JsonProcessingException {
        // Given
        QueryDto parsedQuery = new QueryDto();
        parsedQuery.setMovieName("Parsed Movie");

        QueriesDto additionQueries = new QueriesDto();
        additionQueries.setMovieNameQuery("New Movie");
        additionQueries.setRegionQuery("New Region");
        additionQueries.setDateQuery("2024-02-02");

        String jsonString = "{\"movieName\": \"New Movie\", \"region\": \"New Region\", \"date\": \"2024-02-02\"}";

        PyFunction mockFunction = mock(PyFunction.class);
        PyObject mockPyObject = new PyUnicode(jsonString);

        given(mockFunction.__call__(any(PyObject.class), any(PyObject.class), any(PyObject.class))).willReturn(mockPyObject);
        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(mockFunction);

        // When
        QueryDto result = parseService.parseAdditional(parsedQuery, additionQueries);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getMovieName()).isEqualTo("Parsed Movie"); // This should remain from parsedQuery
        assertThat(result.getRegion()).isEqualTo("New Region");
        assertThat(result.getDate()).isEqualTo("2024-02-02T09:00:00.000");
    }
}