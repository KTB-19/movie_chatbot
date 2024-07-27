package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.QueriesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ParseServiceTest {

    @Autowired
    private ParseService parseService;

    @Test
    @DisplayName("")
    void parse1() {
        QueryDto result = parseService.parseAdditional("query test");
    }

    @Test
    @DisplayName("")
    void parse2() {

        QueryDto parsedQuery = new QueryDto();
        parsedQuery.setMovieName("명량");

        QueriesDto additionQueries = new QueriesDto();
        additionQueries.setMovieNameQuery("null");
        additionQueries.setRegionQuery("구리시");
        additionQueries.setDateQuery("7월 27일");

        QueryDto result = parseService.parseAdditional(parsedQuery, additionQueries);
    }
}