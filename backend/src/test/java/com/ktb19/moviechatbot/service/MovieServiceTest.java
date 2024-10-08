package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.*;
import com.ktb19.moviechatbot.entity.MovieInfo;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import com.ktb19.moviechatbot.feign.AiServerOpenFeign;
import com.ktb19.moviechatbot.repository.MovieInfoRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.sql.Time;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
class MovieServiceTest {

    @InjectMocks
    MovieService movieService;
    @Mock
    MovieInfoRepository movieInfoRepository;
    @Mock
    AiServerOpenFeign aiServerOpenFeign;

    @Test
    @DisplayName("time이 null이면, QueryDto의 movieName, region, date에 해당하는 times를 db에서 조회하여 반환한다")
    void getRunningTimes() {
        //Given
        String movieName = "test movieName";
        String wideArea = "wide";
        String basicArea = "basic";
        LocalDate date = LocalDate.of(2024, 8, 4);

        MovieRunningTimesRequest query = new MovieRunningTimesRequest();
        query.setMovieName(movieName);
        query.setRegion(wideArea + " " + basicArea);
        query.setDate(date);
        query.setTime(null);

        Movie movie = new Movie(1, movieName);
        Theater theater = new Theater(1, "test Theater", wideArea, basicArea);
        LocalTime time1 = LocalTime.of(18, 0);
        LocalTime time2 = LocalTime.of(20, 0);

        MovieInfo movieInfo1 = new MovieInfo(1, movie, theater, date, time1);
        MovieInfo movieInfo2 = new MovieInfo(2, movie, theater, date, time2);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = Map.of(
                theater.getName(), List.of(time1, time2)
        );

        String responseMessage = "message";

        given(movieInfoRepository.findAllByQuery(eq(movieName), eq(wideArea), eq(basicArea), eq(date)))
                .willReturn(List.of(new MovieInfoDetailsQueryDto(movieInfo1, movie, theater), new MovieInfoDetailsQueryDto(movieInfo2, movie, theater)));

        given(aiServerOpenFeign.getRecommend(argThat(request ->
                request.getMovieName().equals(movieName) &&
                request.getDate().equals(date) &&
                request.getTimesPerTheaterNameMap().equals(timesPerTheaterNameMap)
        ))).willReturn(new AiRecommendResponse(responseMessage));

        //When
        MovieRunningTimesDto result = movieService.getRunningTimes(query);

        //Then
        assertThat(result.getMessage()).isEqualTo(responseMessage);
    }

    @Test
    @DisplayName("time이 null이 아니면, time이상의 times를 db에서 조회하여 반환한다")
    void getRunningTimes_with_time() {
        //Given
        String movieName = "test movieName";
        String wideArea = "wide";
        String basicArea = "basic";
        LocalDate date = LocalDate.of(2024, 8, 4);

        MovieRunningTimesRequest query = new MovieRunningTimesRequest();
        query.setMovieName(movieName);
        query.setRegion(wideArea + " " + basicArea);
        query.setDate(date);
        query.setTime(LocalTime.of(19, 0));

        Movie movie = new Movie(1, movieName);
        Theater theater = new Theater(1, "test Theater", wideArea, basicArea);
        LocalTime time1 = LocalTime.of(18, 0);
        LocalTime time2 = LocalTime.of(20, 0);

        MovieInfo movieInfo1 = new MovieInfo(1, movie, theater, date, time1);
        MovieInfo movieInfo2 = new MovieInfo(2, movie, theater, date, time2);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = Map.of(
                theater.getName(), List.of(time2)
        );

        String responseMessage = "message";

        given(movieInfoRepository.findAllByQueryAfterTime(eq(movieName), eq(wideArea), eq(basicArea), eq(date), eq(LocalTime.of(19, 0))))
                .willReturn(List.of(new MovieInfoDetailsQueryDto(movieInfo2, movie, theater)));

        given(aiServerOpenFeign.getRecommend(argThat(request ->
                request.getMovieName().equals(movieName) &&
                        request.getDate().equals(date) &&
                        request.getTimesPerTheaterNameMap().equals(timesPerTheaterNameMap)
        ))).willReturn(new AiRecommendResponse(responseMessage));

        //When
        MovieRunningTimesDto result = movieService.getRunningTimes(query);

        //Then
        assertThat(result.getMessage()).isEqualTo(responseMessage);
    }

    @Test
    @DisplayName("QueryDto의 region을 split 했을 때, 2개로 나눠지지 않으면 IllegalArgumentException을 던진다")
    void getRunningTimes_region_format_exception() {
        //Given
        MovieRunningTimesRequest query = new MovieRunningTimesRequest();
        query.setMovieName("test movieName");
        query.setRegion("경기도구리시");
        query.setDate(LocalDate.of(2024, 8, 4));

        //When
        //Then
        assertThatThrownBy(() -> movieService.getRunningTimes(query))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("QueryDto의 region을 split 했을 때, 첫번째 띄어쓰기를 기준으로 split되어야한다.")
    void getRunningTimes_split_only_first() {
        //Given
        MovieRunningTimesRequest query = new MovieRunningTimesRequest();
        query.setMovieName("test movieName");
        query.setRegion("경상남도 창원시 마산합포구");
        query.setDate(LocalDate.of(2024, 8, 4));

        LocalTime time1 = LocalTime.of(13, 0);
        LocalTime time2 = LocalTime.of(18, 0);

        Movie movie = new Movie(1, "test movieName");
        Theater theater = new Theater(1, "창원CGV", "경상남도", "창원시 마산합포구");
        MovieInfo movieInfo1 = new MovieInfo(1, movie, theater, query.getDate(), time1);
        MovieInfo movieInfo2 = new MovieInfo(1, movie, theater, query.getDate(), time2);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = Map.of(
                theater.getName(), List.of(time1, time2)
        );

        String responseMessage = "message";

        given(movieInfoRepository.findAllByQuery(
                eq(query.getMovieName()),
                eq("경상남도"),
                eq("창원시 마산합포구"),
                eq(query.getDate())
        )).willReturn(List.of(
                new MovieInfoDetailsQueryDto(movieInfo1, movie, theater),
                new MovieInfoDetailsQueryDto(movieInfo2, movie, theater)
        ));

        given(aiServerOpenFeign.getRecommend(argThat(request ->
                request.getMovieName().equals(query.getMovieName()) &&
                        request.getDate().equals(query.getDate()) &&
                        request.getTimesPerTheaterNameMap().equals(timesPerTheaterNameMap)
        ))).willReturn(new AiRecommendResponse(responseMessage));

        //When
        MovieRunningTimesDto result = movieService.getRunningTimes(query);

        //Then
        assertThat(result.getMessage()).isEqualTo(responseMessage);

    }

    @Test
    @DisplayName("QueryDto의 region을 split 했을 때, trim 적용되어야 한다.")
    void getRunningTimes_trim() {
        //Given
        MovieRunningTimesRequest query = new MovieRunningTimesRequest();
        query.setMovieName("test movieName");
        query.setRegion("경상남도  창원시 마산합포구  ");
        query.setDate(LocalDate.of(2024, 8, 4));

        LocalTime time1 = LocalTime.of(13, 0);
        LocalTime time2 = LocalTime.of(18, 0);

        Movie movie = new Movie(1, "test movieName");
        Theater theater = new Theater(1, "창원CGV", "경상남도", "창원시 마산합포구");
        MovieInfo movieInfo1 = new MovieInfo(1, movie, theater, query.getDate(), time1);
        MovieInfo movieInfo2 = new MovieInfo(1, movie, theater, query.getDate(), time2);

        Map<String, List<LocalTime>> timesPerTheaterNameMap = Map.of(
                theater.getName(), List.of(time1, time2)
        );

        String responseMessage = "message";

        given(movieInfoRepository.findAllByQuery(
                eq(query.getMovieName()),
                eq("경상남도"),
                eq("창원시 마산합포구"),
                eq(query.getDate())
        )).willReturn(List.of(
                new MovieInfoDetailsQueryDto(movieInfo1, movie, theater),
                new MovieInfoDetailsQueryDto(movieInfo2, movie, theater)
        ));

        given(aiServerOpenFeign.getRecommend(argThat(request ->
                request.getMovieName().equals(query.getMovieName()) &&
                        request.getDate().equals(query.getDate()) &&
                        request.getTimesPerTheaterNameMap().equals(timesPerTheaterNameMap)
        ))).willReturn(new AiRecommendResponse(responseMessage));

        //When
        MovieRunningTimesDto result = movieService.getRunningTimes(query);

        //Then
        assertThat(result.getMessage()).isEqualTo(responseMessage);
    }
}