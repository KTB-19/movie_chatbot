package com.ktb19.moviechatbot.exception;

import com.ktb19.moviechatbot.exception.common.MovieErrorCode;
import lombok.Getter;

@Getter
public class PyFunctionNotFoundException extends RuntimeException {

    private final MovieErrorCode code;
    private final String requestKey;

    public PyFunctionNotFoundException(String requestKey) {
        this.code = MovieErrorCode.NOT_FOUND_PYFUNCTION;
        this.requestKey = requestKey;
    }
}
