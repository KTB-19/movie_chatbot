package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.AiInfosResponse;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.feign.AiServerOpenFeign;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalTime;

@Service
@RequiredArgsConstructor
@Slf4j
public class ParseService {

    private final AiServerOpenFeign aiServerOpenFeign;

    public QueryDto parse(String message) {

        AiInfosResponse response = aiServerOpenFeign.getInfos(message);
        log.info("parse feign response");
        log.info("response.getMovieName() : " + response.getMovieName());
        log.info("response.getRegion() : " + response.getRegion());
        log.info("response.getDate() : " + response.getDate());
        log.info("response.getTime() : " + response.getTime());
        log.info("response.getResponse() : " + response.getResponse());

        return QueryDto.of(response);
    }

    public QueryDto parseAdditional(AdditionalQueryRequest request) {

        AiInfosResponse response = aiServerOpenFeign.getInfosAdditional(request);
        log.info("parseAdditional feign response");
        log.info("response.getMovieName() : " + response.getMovieName());
        log.info("response.getRegion() : " + response.getRegion());
        log.info("response.getDate() : " + response.getDate());
        log.info("response.getTime() : " + response.getTime());
        log.info("response.getResponse() : " + response.getResponse());

        return QueryDto.of(response);
    }
}
