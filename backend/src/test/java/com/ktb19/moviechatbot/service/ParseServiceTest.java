package com.ktb19.moviechatbot.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ktb19.moviechatbot.dto.QueriesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.exception.FailParsingPyObjectToJsonException;
import com.ktb19.moviechatbot.exception.PyFunctionNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyUnicode;
import org.python.util.PythonInterpreter;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.BDDMockito.*;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.mock;

@ExtendWith(MockitoExtension.class)
class ParseServiceTest {

    @Mock
    private PythonInterpreter pythonInterpreter;
    @Spy
    private ObjectMapper mapper;
    @InjectMocks
    private ParseService parseService;

    @BeforeEach
    void setUp() {
        mapper.registerModule(new JavaTimeModule());
    }

    @Test
    @DisplayName("주어진 메시지를 파싱하여 QueryDto 객체로 반환한다.")
    void testParse() {
        // Given
        String message = "test message";
        String jsonString = "{\"movieName\": \"Test Movie\", \"region\": \"Test Region\", \"date\": \"2024-01-01\"}";

        PyFunction mockFunction = mock(PyFunction.class);
        PyObject mockPyObject = new PyUnicode(jsonString);

        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(mockFunction);
        given(mockFunction.__call__(any(PyObject.class))).willReturn(mockPyObject);
//        willDoNothing().given(pythonInterpreter).execfile("src/main/java/com/ktb19/moviechatbot/ai/test1.py");

        // When
        QueryDto result = parseService.parse(message);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getMovieName()).isEqualTo("Test Movie");
        assertThat(result.getRegion()).isEqualTo("Test Region");
        assertThat(result.getDate()).isEqualTo("2024-01-01");
    }

    @Test
    @DisplayName("pyFunction null이면, PyFunctionNotFoundException 던진다")
    void testParse_pyFunction_not_found() {
        //Given
        String message = "test message";

        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(null);

        //When
        //Then
        assertThatThrownBy(() -> parseService.parse(message))
                .isInstanceOf(PyFunctionNotFoundException.class);
    }

    @Test
    @DisplayName("잘못된 형식의 pyObject가 반환되면, FailParsingPyObjectToJsonException 던진다")
    void testParse_fail_parsing() {
        //Given
        String message = "test message";

        String jsonString = "{\"wrongName\": \"Test Movie\", \"region\": \"Test Region\", \"date\": \"2024-01-01\"}";

        PyFunction mockFunction = mock(PyFunction.class);
        PyObject mockPyObject = new PyUnicode(jsonString);

        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(mockFunction);
        given(mockFunction.__call__(any(PyObject.class))).willReturn(mockPyObject);
//        willDoNothing().given(pythonInterpreter).execfile("src/main/java/com/ktb19/moviechatbot/ai/test1.py");

        //When
        //Then
        assertThatThrownBy(() -> parseService.parse(message))
                .isInstanceOf(FailParsingPyObjectToJsonException.class);
    }

    @Test
    @DisplayName("추가 쿼리를 파싱하여 기존 parsedQuery와 병합된 QueryDto 객체로 반환한다.")
    void testParseAdditional() {
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
        assertThat(result.getDate()).isEqualTo("2024-02-02");
    }

    @Test
    @DisplayName("pyFunction null이면, PyFunctionNotFoundException 던진다")
    void testParseAdditional_pyFunction_not_found() {
        //Given
        QueryDto parsedQuery = new QueryDto();
        parsedQuery.setMovieName("Parsed Movie");

        QueriesDto additionQueries = new QueriesDto();
        additionQueries.setMovieNameQuery("New Movie");
        additionQueries.setRegionQuery("New Region");
        additionQueries.setDateQuery("2024-02-02");

        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(null);

        //When
        //Then
        assertThatThrownBy(() -> parseService.parseAdditional(parsedQuery, additionQueries))
                .isInstanceOf(PyFunctionNotFoundException.class);
    }

    @Test
    @DisplayName("잘못된 형식의 pyObject가 반환되면, FailParsingPyObjectToJsonException 던진다")
    void testParseAdditional_fail_parsing() {
        //Given
        QueryDto parsedQuery = new QueryDto();
        parsedQuery.setMovieName("Parsed Movie");

        QueriesDto additionQueries = new QueriesDto();
        additionQueries.setMovieNameQuery("New Movie");
        additionQueries.setRegionQuery("New Region");
        additionQueries.setDateQuery("2024-02-02");

        String jsonString = "{\"wrongName\": \"New Movie\", \"region\": \"New Region\", \"date\": \"2024-02-02\"}";

        PyFunction mockFunction = mock(PyFunction.class);
        PyObject mockPyObject = new PyUnicode(jsonString);

        given(mockFunction.__call__(any(PyObject.class), any(PyObject.class), any(PyObject.class))).willReturn(mockPyObject);
        given(pythonInterpreter.get(anyString(), eq(PyFunction.class))).willReturn(mockFunction);

        //When
        //Then
        assertThatThrownBy(() -> parseService.parseAdditional(parsedQuery, additionQueries))
                .isInstanceOf(FailParsingPyObjectToJsonException.class);
    }
}