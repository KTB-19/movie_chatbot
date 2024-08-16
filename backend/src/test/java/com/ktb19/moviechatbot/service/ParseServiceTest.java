package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.AiInfosResponse;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.feign.AiServerOpenFeign;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
class ParseServiceTest {

    @InjectMocks
    private ParseService parseService;

    @Mock
    private AiServerOpenFeign aiServerOpenFeign;

    @Test
    @DisplayName("날짜 parse test")
    void parse() {
        //Given
        AiInfosResponse response = new AiInfosResponse(
                "2023 심규선 단독 콘서트 : 우리 앞의 세계",
                null,
                "2024-08-19",
                "16:00",
                "어느 지역에서 영화를 보고 싶으신가요?"
        );
        given(aiServerOpenFeign.getInfos(anyString())).willReturn(response);

        //When
        QueryDto dto = parseService.parse("question");

        //Then
        System.out.println(dto.getDate());
        System.out.println(dto.getTime());

    }

    @Test
    void parseAdditional() {
    }
}