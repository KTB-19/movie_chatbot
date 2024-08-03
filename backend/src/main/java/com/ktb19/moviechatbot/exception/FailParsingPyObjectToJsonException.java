package com.ktb19.moviechatbot.exception;

import com.ktb19.moviechatbot.exception.common.MovieErrorCode;
import lombok.Getter;

@Getter
public class FailParsingPyObjectToJsonException extends RuntimeException {

    private final MovieErrorCode code;
    private final String requestKey;

    public FailParsingPyObjectToJsonException(String requestKey) {
        this.code = MovieErrorCode.FAIL_PARSING_PYOBJECT_TO_JSON;
        this.requestKey = requestKey;
    }
}
