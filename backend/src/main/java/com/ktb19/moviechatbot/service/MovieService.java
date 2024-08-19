package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.*;
import com.ktb19.moviechatbot.repository.MovieInfoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.sql.Time;
import java.time.LocalTime;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static java.util.stream.Collectors.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class MovieService {

    private final MovieInfoRepository movieInfoRepository;

    public MovieRunningTimesDto getRunningTimes(MovieRunningTimesRequest query) {

        String[] areas = parseRegionToAreas(query.getRegion());

        List<MovieInfoDetailsQueryDto> dto = getMovieInfoDetails(query, areas);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = dto.stream()
                .collect(groupingBy(d -> d.getTheater().getName(), mapping(d -> d.getMovieInfo().getTime(), toList())));
        log.info("timesPerTheaterNameMap : " + timesPerTheaterNameMap);

        List<TheaterRunningTimesDto> theaterRunningTimesDtos = timesPerTheaterNameMap.entrySet().stream()
                .map(e -> new TheaterRunningTimesDto(e.getKey(), e.getValue().size(), e.getValue()))
                .toList();
        log.info("theaterRunningTimesDtos : " + theaterRunningTimesDtos);

        return new MovieRunningTimesDto(theaterRunningTimesDtos.size(), theaterRunningTimesDtos);
    }

    private List<MovieInfoDetailsQueryDto> getMovieInfoDetails(MovieRunningTimesRequest query, String[] areas) {
        if (query.getTime() == null) {
            return movieInfoRepository.findAllByQuery(
                    query.getMovieName(),
                    areas[0],
                    areas[1],
                    query.getDate()
            );
        }

        return movieInfoRepository.findAllByQueryAfterTime(
                query.getMovieName(),
                areas[0],
                areas[1],
                query.getDate(),
                query.getTime()
        );
    }

    private static String[] parseRegionToAreas(String region) {
        String[] areas = region.split(" ", 2);
        if (areas.length != 2) {
            throw new IllegalArgumentException("잘못된 region 형식입니다.");
        }

        return Arrays.stream(areas)
                .map(String::trim)
                .toArray(String[]::new);
    }
}
