package com.ktb19.moviechatbot.exception;

import com.ktb19.moviechatbot.exception.common.GlobalErrorCode;
import lombok.Getter;

@Getter
public class PyFunctionNotFoundException extends RuntimeException {

    private final GlobalErrorCode code;
    private final String requestKey;

    public PyFunctionNotFoundException(String requestKey) {
        this.code = GlobalErrorCode.NOT_FOUND_PYFUNCTION;
        this.requestKey = requestKey;
    }
}
