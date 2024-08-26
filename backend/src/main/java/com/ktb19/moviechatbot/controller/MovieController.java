package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.MovieRunningTimesRequest;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.service.MovieService;
import com.ktb19.moviechatbot.service.ParseService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 영화 관련 쿼리와 상영 시간 정보를 처리하는 API를 제공합니다.
 */
@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class MovieController {

    private final ParseService parseService;
    private final MovieService movieService;

    /**
     * 메시지를 파싱하여 영화 이름, 지역, 날짜, 시간을 추출합니다.
     *
     * @param message 한글, 영어, 숫자 및 일부 특수문자로 구성된 메시지
     * @return 파싱된 결과를 포함한 ResponseEntity 객체
     */
    @GetMapping("/movie/query")
    public ResponseEntity<?> getParsedQuery(
            @RequestParam
            @Size(min = 1, max = 200)
            @Pattern(
                    regexp = "^[가-힣a-zA-Z0-9 !#$%&'*+/=?`{|}~^.-:]*$",
                    message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다."
            )
            String message) {

        return ResponseEntity.ok(parseService.parse(message));
    }

    /**
     * 이미 파싱된 객체와 메시지를 같이 받아, 완성된 영화 이름, 지역, 날짜, 시간이 포함된 객체를 반환합니다.
     *
     * @param request 추가 쿼리 객체와 메시지를 담고 있는 AdditionalQueryRequest 객체
     * @return 파싱된 쿼리 결과를 포함한 ResponseEntity 객체
     */
    @PostMapping("/movie/query/additional")
    public ResponseEntity<?> getParsedQueryByAdditionalQuery(@RequestBody @Valid AdditionalQueryRequest request) {
        return ResponseEntity.ok(parseService.parseAdditional(request));
    }

    /**
     * 영화의 상영 시간을 조회합니다.
     *
     * @param parsedQuery 파싱된 객체 정보를 담고 있는 MovieRunningTimesRequest 객체
     * @return 상영 시간 정보를 포함한 ResponseEntity 객체
     */
    @PostMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody @Valid MovieRunningTimesRequest parsedQuery) {
        return ResponseEntity.ok(movieService.getRunningTimes(parsedQuery));
    }
}
