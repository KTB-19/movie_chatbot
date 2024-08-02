package com.ktb19.moviechatbot.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ktb19.moviechatbot.dto.*;
import com.ktb19.moviechatbot.service.MovieService;
import com.ktb19.moviechatbot.service.ParseService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
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

    @GetMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody MovieRunningTimeRequest request) {

        QueryDto query = parseService.parseAdditional(request.getParsedQuery(), request.getAdditionQueries());
        log.info("query.getMovieName() = {}", query.getMovieName());
        log.info("query.getRegion() = {}", query.getRegion());
        log.info("query.getDate() = {}", query.getDate());

        RunningTimesDto runningTimesDto = movieService.getRunningTimes(query);

        return ResponseEntity.ok(new MovieRunningTimeResponse(runningTimesDto.getTimes().size(), runningTimesDto.getTimes()));
    }
}
