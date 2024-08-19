package com.ktb19.moviechatbot.exception.common;

import com.ktb19.moviechatbot.exception.FailParsingPyObjectToJsonException;
import com.ktb19.moviechatbot.exception.PyFunctionNotFoundException;
import feign.FeignException;
import feign.RetryableException;
import feign.codec.DecodeException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {


    @ExceptionHandler(PyFunctionNotFoundException.class)
    public ResponseEntity<ErrorResponse> handlePyFunctionNotFoundException(PyFunctionNotFoundException e) {
        log.error("PyFunctionNotFoundException functionName = {}", e.getRequestKey(), e);

        ErrorCode errorCode = e.getCode();
        return ResponseEntity.status(errorCode.getHttpStatus())
                .body(ErrorResponse.of(errorCode));
    }

    @ExceptionHandler(FailParsingPyObjectToJsonException.class)
    public ResponseEntity<ErrorResponse> handleFailParsingPyObjectToJsonException(FailParsingPyObjectToJsonException e) {
        log.error("FailParsingPyObjectToJsonException pyObject = {}", e.getRequestKey(), e);

        ErrorCode errorCode = e.getCode();
        return ResponseEntity.status(errorCode.getHttpStatus())
                .body(ErrorResponse.of(errorCode));
    }

    @ExceptionHandler(FeignException.class)
    public ResponseEntity<ErrorResponse> handleFeignException(FeignException e) {

        if (e instanceof DecodeException) {
            log.warn("잘못된 argument");
        }
        if (e instanceof RetryableException) {
            log.warn("api 종료 상태");
        }

        log.error("FeignException status = {}", e.status(), e);

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ErrorResponse.of(GlobalErrorCode.SERVER_ERROR));
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException e) {
        log.warn("HttpMessageNotReadableException 잘못된 입력 JSON Format", e);

        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ErrorResponse.of(GlobalErrorCode.BAD_REQUEST));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleOtherException(Exception e) {
        log.error("Exception", e);

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ErrorResponse.of(GlobalErrorCode.SERVER_ERROR));
    }
}
