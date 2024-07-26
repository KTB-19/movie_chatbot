package com.ktb19.moviechatbot.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class MovieRunningTimeRequest {

    private QueryDto parsedQuery;
    private QueriesDto additionQueries;
}
