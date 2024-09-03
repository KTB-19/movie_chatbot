package com.ktb19.moviechatbot.exception;

import com.ktb19.moviechatbot.exception.common.GlobalErrorCode;
import lombok.Getter;

@Getter
public class FailParsingPyObjectToJsonException extends RuntimeException {

    private final GlobalErrorCode code;
    private final String requestKey;

    public FailParsingPyObjectToJsonException(String requestKey) {
        this.code = GlobalErrorCode.FAIL_PARSING_PYOBJECT_TO_JSON;
        this.requestKey = requestKey;
    }
}
