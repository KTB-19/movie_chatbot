package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.dto.MovieInfoDetailsQueryDto;
import com.ktb19.moviechatbot.entity.MovieInfo;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MovieInfoRepositoryTest {

    @Autowired
    MovieInfoRepository movieInfoRepository;

    @Autowired
    MovieRepository movieRepository;

    @Autowired
    TheaterRepository theaterRepository;

    private Movie movie1, movie2;
    private Theater theater1, theater2;

    @BeforeEach
    void setUp() {
        movie1 = Movie.builder().id(1).title("test title1").build();
        movie1 = movieRepository.save(movie1);

        movie2 = Movie.builder().id(2).title("test title2").build();
        movie2 = movieRepository.save(movie2);

        theater1 = Theater.builder().id(1).wideArea("test wideArea1").basicArea("test basicArea1").build();
        theater1 = theaterRepository.save(theater1);

        theater2 = Theater.builder().id(2).wideArea("test wideArea2").basicArea("test basicArea2").build();
        theater2 = theaterRepository.save(theater2);
    }

    @Test
    @DisplayName("Info 엔티티 저장 및 조회 테스트")
    void saveAndFindByIdTest() {

        //Given
        MovieInfo movieInfo = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(LocalDate.now())
                .time(LocalTime.of(12, 0))
                .build();

        movieInfoRepository.save(movieInfo);

        //When
        Optional<MovieInfo> foundInfo = movieInfoRepository.findById(Long.valueOf(movieInfo.getId()));

        //Then
        assertThat(foundInfo).isPresent();
        assertThat(foundInfo.get().getMovie()).isEqualTo(movie1);
        assertThat(foundInfo.get().getTheater()).isEqualTo(theater1);
        assertThat(foundInfo.get().getDate()).isEqualTo(movieInfo.getDate());
        assertThat(foundInfo.get().getTime()).isEqualTo(movieInfo.getTime());
    }

    @Test
    @DisplayName("movieName 일치하는 info list를 반환한다.")
    void findAllByQuery_movieName() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        LocalTime time = LocalTime.of(12, 0);

        MovieInfo movieInfo1 = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        MovieInfo movieInfo2 = MovieInfo.builder()
                .id(2)
                .movie(movie2)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        MovieInfo savedMovieInfo1 = movieInfoRepository.save(movieInfo1);
        MovieInfo savedMovieInfo2 = movieInfoRepository.save(movieInfo2);

        //When
        List<MovieInfoDetailsQueryDto> result = movieInfoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(result).hasSize(1);
        assertThat(result.getFirst().getMovieInfo()).isEqualTo(savedMovieInfo1);
        assertThat(result.getFirst().getMovie()).isEqualTo(movie1);
        assertThat(result.getFirst().getTheater()).isEqualTo(theater1);

    }

    @Test
    @DisplayName("wideArea, basicArea 일치하는 info list를 반환한다.")
    void findAllByQuery_wideArea_basicArea() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        LocalTime time = LocalTime.of(12, 0);

        MovieInfo movieInfo1 = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        MovieInfo movieInfo2 = MovieInfo.builder()
                .id(2)
                .movie(movie1)
                .theater(theater2)
                .date(date)
                .time(time)
                .build();

        MovieInfo savedMovieInfo1 = movieInfoRepository.save(movieInfo1);
        MovieInfo savedMovieInfo2 = movieInfoRepository.save(movieInfo2);

        //When
        List<MovieInfoDetailsQueryDto> result = movieInfoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(result).hasSize(1);
        assertThat(result.getFirst().getMovieInfo()).isEqualTo(savedMovieInfo1);
        assertThat(result.getFirst().getMovie()).isEqualTo(movie1);
        assertThat(result.getFirst().getTheater()).isEqualTo(theater1);

    }

    @Test
    @DisplayName("date 일치하는 info list를 반환한다.")
    void findAllByQuery_date() {

        //Given
        LocalDate date1 = LocalDate.of(2024, 8, 1);
        LocalDate date2 = LocalDate.of(2024, 8, 2);
        LocalTime time = LocalTime.of(12, 0);

        MovieInfo movieInfo1 = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date1)
                .time(time)
                .build();

        MovieInfo movieInfo2 = MovieInfo.builder()
                .id(2)
                .movie(movie1)
                .theater(theater1)
                .date(date2)
                .time(time)
                .build();

        MovieInfo savedMovieInfo1 = movieInfoRepository.save(movieInfo1);
        MovieInfo savedMovieInfo2 = movieInfoRepository.save(movieInfo2);

        //When
        List<MovieInfoDetailsQueryDto> result = movieInfoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date1);

        //Then
        assertThat(result).hasSize(1);
        assertThat(result.getFirst().getMovieInfo()).isEqualTo(savedMovieInfo1);
        assertThat(result.getFirst().getMovie()).isEqualTo(movie1);
        assertThat(result.getFirst().getTheater()).isEqualTo(theater1);

    }

    @Test
    @DisplayName("movieName, wideArea, basicArea, date 일치하는 info list를 반환한다.")
    void findAllByQuery_all() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        LocalTime time1 = LocalTime.of(12, 0);
        LocalTime time2 = LocalTime.of(13, 0);

        MovieInfo movieInfo1 = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time1)
                .build();

        MovieInfo movieInfo2 = MovieInfo.builder()
                .id(2)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time2)
                .build();

        MovieInfo savedMovieInfo1 = movieInfoRepository.save(movieInfo1);
        MovieInfo savedMovieInfo2 = movieInfoRepository.save(movieInfo2);

        //When
        List<MovieInfoDetailsQueryDto> result = movieInfoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(result).hasSize(2);
        assertThat(result.getFirst().getMovieInfo()).isEqualTo(savedMovieInfo1);
        assertThat(result.getLast().getMovieInfo()).isEqualTo(savedMovieInfo2);

    }

    @Test
    @DisplayName("주어진 time 이상의 row들을 반환한다.")
    void findAllByQueryAfterTime() {
        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        LocalTime time1 = LocalTime.of(12, 0);
        LocalTime time2 = LocalTime.of(13, 30);
        LocalTime time3 = LocalTime.of(15, 0);

        MovieInfo movieInfo1 = MovieInfo.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time1)
                .build();

        MovieInfo movieInfo2 = MovieInfo.builder()
                .id(2)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time2)
                .build();

        MovieInfo movieInfo3 = MovieInfo.builder()
                .id(3)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time3)
                .build();


        MovieInfo savedMovieInfo1 = movieInfoRepository.save(movieInfo1);
        MovieInfo savedMovieInfo2 = movieInfoRepository.save(movieInfo2);
        MovieInfo savedMovieInfo3 = movieInfoRepository.save(movieInfo3);

        //When
        List<MovieInfoDetailsQueryDto> result = movieInfoRepository.findAllByQueryAfterTime(
                movie1.getTitle(),
                theater1.getWideArea(),
                theater1.getBasicArea(),
                date,
                LocalTime.of(13, 30));

        //Then
        assertThat(result).hasSize(2);
        assertThat(result.getFirst().getMovieInfo()).isEqualTo(savedMovieInfo2);
        assertThat(result.getLast().getMovieInfo()).isEqualTo(savedMovieInfo3);
    }
}