package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.repository.InfoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MovieService {

    private final InfoRepository infoRepository;

    public void getRunningTimes(QueryDto query) {

    }
}
