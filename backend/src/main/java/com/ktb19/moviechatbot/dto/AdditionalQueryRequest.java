package com.ktb19.moviechatbot.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AdditionalQueryRequest {

    private QueryDto parsedQuery;
    private String message;
}
