package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.service.ParseService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class QueryController {

    private final ParseService parseService;

    @GetMapping("/query")
    public ResponseEntity<?> query(@RequestParam String query) {

        QueryDto dto = parseService.parse(query);

        return ResponseEntity.ok().build();
    }
}
