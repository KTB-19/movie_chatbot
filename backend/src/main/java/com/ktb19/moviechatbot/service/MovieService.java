package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.MovieRunningTimesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.dto.TheaterRunningTimesDto;
import com.ktb19.moviechatbot.dto.InfoDetailsQueryDto;
import com.ktb19.moviechatbot.repository.InfoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.sql.Time;
import java.util.List;
import java.util.Map;

import static java.util.stream.Collectors.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class MovieService {

    private final InfoRepository infoRepository;

    public MovieRunningTimesDto getRunningTimes(QueryDto query) {

        String[] areas = parseRegionToAreas(query.getRegion());
        String wideArea = areas[0];
        String basicArea = areas[1];

        List<InfoDetailsQueryDto> dto =  infoRepository.findAllByQuery(
                query.getMovieName(),
                wideArea,
                basicArea,
                query.getDate()
        );

        Map<String, List<Time>> timesPerTheaterNameMap = dto.stream()
                .collect(groupingBy(d -> d.getTheater().getName(), mapping(d -> d.getInfo().getTime(), toList())));
        log.info("timesPerTheaterNameMap : " + timesPerTheaterNameMap);

        List<TheaterRunningTimesDto> theaterRunningTimesDtos = timesPerTheaterNameMap.entrySet().stream()
                .map(e -> new TheaterRunningTimesDto(e.getKey(), e.getValue().size(), e.getValue()))
                .toList();
        log.info("theaterRunningTimesDtos : " + theaterRunningTimesDtos);

        return new MovieRunningTimesDto(theaterRunningTimesDtos.size(), theaterRunningTimesDtos);
    }

    private static String[] parseRegionToAreas(String region) {
        String[] areas = region.split(" ");
        if (areas.length != 2) {
            throw new IllegalArgumentException("잘못된 region 형식입니다.");
        }

        return areas;
    }
}
