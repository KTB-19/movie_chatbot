package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.QueryDto;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.BDDMockito.given;

@SpringBootTest
class ParseServiceTest {

    @Autowired
    private ParseService parseService;

    @Test
    @DisplayName("")
    void parse() {
        QueryDto result = parseService.parse("query test");
    }
}