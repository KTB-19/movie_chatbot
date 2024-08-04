package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.MovieRunningTimeResponse;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.dto.RunningTimesDto;
import com.ktb19.moviechatbot.service.MovieService;
import com.ktb19.moviechatbot.service.ParseService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequiredArgsConstructor
public class MovieController {

    private final ParseService parseService;
    private final MovieService movieService;

    @GetMapping("/movie/query")
    public ResponseEntity<?> getParsedQuery(@RequestParam String message) {
        return ResponseEntity.ok(parseService.parse(message));
    }

    @GetMapping("/movie/query/additional")
    public ResponseEntity<?> getParsedQueryByAdditionalQuery(@RequestBody AdditionalQueryRequest request) {
        return ResponseEntity.ok(parseService.parseAdditional(request.getParsedQuery(), request.getAdditionQueries()));
    }

    @GetMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody QueryDto parsedQuery) {

        RunningTimesDto dto = movieService.getRunningTimes(parsedQuery);

        return ResponseEntity.ok(new MovieRunningTimeResponse(dto.getTimes().size(), dto.getTimes()));
    }
}
