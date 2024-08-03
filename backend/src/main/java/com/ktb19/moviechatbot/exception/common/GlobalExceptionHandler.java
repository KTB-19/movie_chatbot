package com.ktb19.moviechatbot.exception.common;

import com.ktb19.moviechatbot.exception.FailParsingPyObjectToJsonException;
import com.ktb19.moviechatbot.exception.PyFunctionNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {


    @ExceptionHandler(PyFunctionNotFoundException.class)
    public ResponseEntity<Object> handlePyFunctionNotFoundException(PyFunctionNotFoundException e) {
        log.error("PyFunctionNotFoundException functionName = {}", e.getRequestKey(), e);

        ErrorCode errorCode = e.getCode();
        return ResponseEntity.status(errorCode.getHttpStatus())
                .body(ErrorResponse.of(errorCode));
    }

    @ExceptionHandler(FailParsingPyObjectToJsonException.class)
    public ResponseEntity<Object> handleFailParsingPyObjectToJsonException(FailParsingPyObjectToJsonException e) {
        log.error("FailParsingPyObjectToJsonException pyObject = {}", e.getRequestKey(), e);

        ErrorCode errorCode = e.getCode();
        return ResponseEntity.status(errorCode.getHttpStatus())
                .body(ErrorResponse.of(errorCode));
    }
}
