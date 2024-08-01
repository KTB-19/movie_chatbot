package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.dto.RunningTimesDto;
import com.ktb19.moviechatbot.entity.Info;
import com.ktb19.moviechatbot.repository.InfoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.sql.Time;
import java.util.List;

@Service
@RequiredArgsConstructor
public class MovieService {

    private final InfoRepository infoRepository;

    public RunningTimesDto getRunningTimes(QueryDto query) {

        String[] areas = parseRegionToAreas(query.getRegion());
        String wideArea = areas[0];
        String basicArea = areas[1];

        List<Info> findInfos =  infoRepository.findAllByQuery(
                query.getMovieName(),
                wideArea,
                basicArea,
                query.getDate()
        );

        List<Time> times = findInfos.stream()
                .map(Info::getTime)
                .toList();

        return new RunningTimesDto(times);
    }

    private static String[] parseRegionToAreas(String region) {
        return region.split(" ");
    }
}
