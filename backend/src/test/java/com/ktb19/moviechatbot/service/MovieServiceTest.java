package com.ktb19.moviechatbot.service;

import com.ktb19.moviechatbot.dto.MovieInfoDetailsQueryDto;
import com.ktb19.moviechatbot.dto.MovieRunningTimesDto;
import com.ktb19.moviechatbot.dto.QueryDto;
import com.ktb19.moviechatbot.entity.MovieInfo;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import com.ktb19.moviechatbot.repository.MovieInfoRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.sql.Time;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
class MovieServiceTest {

    @InjectMocks
    MovieService movieService;
    @Mock
    MovieInfoRepository movieInfoRepository;

    @Test
    @DisplayName("QueryDto의 movieName, region, date에 해당하는 times를 db에서 조회하여 반환한다")
    void getRunningTimes() {
        //Given
        String movieName = "test movieName";
        String wideArea = "wide";
        String basicArea = "basic";
        LocalDate date = LocalDate.of(2024, 8, 4);

        QueryDto query = new QueryDto();
        query.setMovieName(movieName);
        query.setRegion(wideArea + " " + basicArea);
        query.setDate(date);

        Movie movie = new Movie(1, movieName);
        Theater theater = new Theater(1, "test Theater", wideArea, basicArea);
        Time time1 = Time.valueOf("18:00:00");
        Time time2 = Time.valueOf("20:00:00");

        MovieInfo movieInfo1 = new MovieInfo(1, movie, theater, date, time1);
        MovieInfo movieInfo2 = new MovieInfo(2, movie, theater, date, time2);

        given(movieInfoRepository.findAllByQuery(eq(movieName), eq(wideArea), eq(basicArea), eq(date)))
                .willReturn(List.of(new MovieInfoDetailsQueryDto(movieInfo1, movie, theater), new MovieInfoDetailsQueryDto(movieInfo2, movie, theater)));

        //When
        MovieRunningTimesDto result = movieService.getRunningTimes(query);

        //Then
        assertThat(result.getCount()).isEqualTo(1);
        assertThat(result.getTheaterRunningTimes().getFirst().getCount()).isEqualTo(2);
        assertThat(result.getTheaterRunningTimes().getFirst().getTimes()).contains(time1, time2);
    }

    @Test
    @DisplayName("QueryDto의 region을 split 했을 때, 2개로 나눠지지 않으면 IllegalArgumentException을 던진다")
    void getRunningTimes_region_format_exception() {
        //Given
        QueryDto query = new QueryDto();
        query.setMovieName("test movieName");
        query.setRegion("경기도구리시");
        query.setDate(LocalDate.of(2024, 8, 4));

        //When
        //Then
        assertThatThrownBy(() -> movieService.getRunningTimes(query))
                .isInstanceOf(IllegalArgumentException.class);
    }
}