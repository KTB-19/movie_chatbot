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

/**
 * AI 서버와 통신을 통해, 파싱 된 결과를 반환하는 서비스 클래스입니다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class ParseService {

    private final AiServerOpenFeign aiServerOpenFeign;

    /**
     * AI 서버를 통해, 사용자의 메시지를 파싱하여 반환합니다.
     *
     * @param message 사용자가 입력한 메시지
     * @return 파싱된 정보를 담은 QueryDto 객체
     */
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

    /**
     * 파싱된 쿼리와 추가적인 메시지를 담은 요청을 AI 서버를 통해 파싱하여 반환합니다.
     *
     * @param request 파싱된 쿼리와 추가적인 메시지를 담고 있는 AdditionalQueryRequest 객체
     * @return 파싱된 정보를 담은 QueryDto 객체
     */
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
