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

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class MovieController {

    private final ParseService parseService;
    private final MovieService movieService;

    @GetMapping("/movie/query")
    public ResponseEntity<?> getParsedQuery(
            @RequestParam
            @Size(min = 1, max = 200)
            @Pattern(
                    regexp = "^[가-힣a-zA-Z0-9 !#$%&'*+/=?`{|}~^.-]*$",
                    message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다."
            )
            String message) {

        return ResponseEntity.ok(parseService.parse(message));
    }

    @GetMapping("/movie/query/additional")
    public ResponseEntity<?> getParsedQueryByAdditionalQuery(@RequestBody @Valid AdditionalQueryRequest request) {
        return ResponseEntity.ok(parseService.parseAdditional(request));
    }

    @GetMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody @Valid MovieRunningTimesRequest parsedQuery) {
        return ResponseEntity.ok(movieService.getRunningTimes(parsedQuery));
    }
}
