package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.service.MovieService;
import com.ktb19.moviechatbot.service.ParseService;
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
    public ResponseEntity<?> getParsedQuery(@RequestParam String message) {
        return ResponseEntity.ok(parseService.parse(message));
    }

    @GetMapping("/movie/query/additional")
    public ResponseEntity<?> getParsedQueryByAdditionalQuery(@RequestBody AdditionalQueryRequest request) {
        return ResponseEntity.ok(parseService.parseAdditional(request));
    }

    @GetMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody QueryDto parsedQuery) {
        return ResponseEntity.ok(movieService.getRunningTimes(parsedQuery));
    }
}
