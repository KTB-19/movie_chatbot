package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.MovieRunningTimeRequest;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.service.ParseService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class MovieController {

    private final ParseService parseService;

    @GetMapping("/movie/query")
    public ResponseEntity<?> getParsedQuery(@RequestParam String message) {
        return ResponseEntity.ok(parseService.parseAdditional(message));
    }

    @GetMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(@RequestBody MovieRunningTimeRequest request) {

        //parse
        QueryDto dto = parseService.parseAdditional(request.getParsedQuery(), request.getAdditionQueries());

        //db에서 상영정보 가져오기

        return ResponseEntity.ok().build();
    }
}
