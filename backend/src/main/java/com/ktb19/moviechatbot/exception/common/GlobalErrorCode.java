package com.ktb19.moviechatbot.exception.common;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum GlobalErrorCode implements ErrorCode {

    NOT_FOUND_PYFUNCTION(HttpStatus.INTERNAL_SERVER_ERROR, "PyFunction Not Found"),
    FAIL_PARSING_PYOBJECT_TO_JSON(HttpStatus.INTERNAL_SERVER_ERROR, "Fail to parse PyObject to JSON"),

    SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "서버에서 알 수 없는 에러 발생"),
    ;

    private final HttpStatus httpStatus;
    private final String message;

}
