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

/**
 * 영화 상영 시간 정보를 제공하는 서비스 클래스입니다.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MovieService {

    private final MovieInfoRepository movieInfoRepository;

    /**
     * 영화 이름, 지역, 날짜, 시간을 통해 상영 시간을 조회하고, 극장별로 그룹화하여 반환합니다.
     *
     * @param query 영화 이름, 지역, 날짜, 시간을 담고 있는 MovieRunningTimesRequest 객체
     * @return 극장별 상영 시간 정보를 담은 MovieRunningTimesDto 객체
     */
    public MovieRunningTimesDto getRunningTimes(MovieRunningTimesRequest query) {

        String[] areas = parseRegionToAreas(query.getRegion());

        List<MovieInfoDetailsQueryDto> dto = getMovieInfoDetails(query, areas);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = groupByTheater(dto);
        log.info("timesPerTheaterNameMap : " + timesPerTheaterNameMap);

        List<TheaterRunningTimesDto> theaterRunningTimesDtos = mappingToDto(timesPerTheaterNameMap);
        log.info("theaterRunningTimesDtos : " + theaterRunningTimesDtos);

        return new MovieRunningTimesDto(theaterRunningTimesDtos.size(), theaterRunningTimesDtos);
    }

    /**
     * 주어진 지역 정보를 파싱하여 두 개의 지역 문자열 배열로 반환합니다.
     *
     * @param region 지역 정보를 담은 문자열
     * @return 파싱된 두 개의 지역 문자열 배열
     * @throws IllegalArgumentException 지역 정보 형식이 잘못된 경우 예외를 발생시킵니다.
     */
    private static String[] parseRegionToAreas(String region) {
        String[] areas = region.split(" ", 2);
        if (areas.length != 2) {
            throw new IllegalArgumentException("잘못된 region 형식입니다.");
        }

        return Arrays.stream(areas)
                .map(String::trim)
                .toArray(String[]::new);
    }

    /**
     * 주어진 요청과 지역 정보를 바탕으로 영화 정보 상세 리스트를 조회합니다.
     * 요청에서 time이 존재하면, time 이상의 상영 시간을 반환합니다.
     * time이 존재하지 않으면, 당일의 모든 상영 시간을 반환합니다.
     *
     * @param query 영화 상영 시간 조회 요청을 담고 있는 MovieRunningTimesRequest 객체
     * @param areas 파싱된 지역 문자열 배열
     * @return 조회된 영화 정보 상세 리스트
     */
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

    /**
     * 조회된 영화 정보 리스트를 극장 이름별로 그룹화합니다.
     *
     * @param dto 영화 정보 상세 리스트
     * @return 극장 이름별로 그룹화된 상영 시간 맵
     */
    private Map<String, List<LocalTime>> groupByTheater(List<MovieInfoDetailsQueryDto> dto) {
        return dto.stream()
                .collect(
                        groupingBy(
                                d -> d.getTheater().getName(),
                                mapping(d -> d.getMovieInfo().getTime(), toList())
                        ));
    }

    /**
     * 극장별 상영 시간 맵을 DTO 리스트로 변환합니다.
     *
     * @param timesPerTheaterNameMap 극장 이름별 상영 시간 맵
     * @return 극장별 상영 시간 정보를 담은 DTO 리스트
     */
    private List<TheaterRunningTimesDto> mappingToDto(Map<String, List<LocalTime>> timesPerTheaterNameMap) {
        return timesPerTheaterNameMap.entrySet().stream()
                .map(e -> new TheaterRunningTimesDto(e.getKey(), e.getValue().size(), e.getValue()))
                .toList();
    }
}
