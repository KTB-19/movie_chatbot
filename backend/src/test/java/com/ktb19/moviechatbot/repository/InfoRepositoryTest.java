package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.entity.Info;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.sql.Date;
import java.sql.Time;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class InfoRepositoryTest {

    @Autowired
    InfoRepository infoRepository;

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
        Info info = Info.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(LocalDate.now())
                .time(Time.valueOf("12:00:00"))
                .build();

        infoRepository.save(info);

        //When
        Optional<Info> foundInfo = infoRepository.findById(Long.valueOf(info.getId()));

        //Then
        assertThat(foundInfo).isPresent();
        assertThat(foundInfo.get().getMovie()).isEqualTo(movie1);
        assertThat(foundInfo.get().getTheater()).isEqualTo(theater1);
        assertThat(foundInfo.get().getDate()).isEqualTo(info.getDate());
        assertThat(foundInfo.get().getTime()).isEqualTo(info.getTime());
    }

    @Test
    @DisplayName("movieName 일치하는 info list를 반환한다.")
    void findAllByQuery_movieName() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        Time time = Time.valueOf("12:00:00");

        Info info1 = Info.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        Info info2 = Info.builder()
                .id(2)
                .movie(movie2)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        Info savedInfo1 = infoRepository.save(info1);
        Info savedInfo2 = infoRepository.save(info2);

        //When
        List<Info> findInfos = infoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(findInfos).hasSize(1);
        assertThat(findInfos.getFirst()).isEqualTo(savedInfo1);

    }

    @Test
    @DisplayName("wideArea, basicArea 일치하는 info list를 반환한다.")
    void findAllByQuery_wideArea_basicArea() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        Time time = Time.valueOf("12:00:00");

        Info info1 = Info.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time)
                .build();

        Info info2 = Info.builder()
                .id(2)
                .movie(movie1)
                .theater(theater2)
                .date(date)
                .time(time)
                .build();

        Info savedInfo1 = infoRepository.save(info1);
        Info savedInfo2 = infoRepository.save(info2);

        //When
        List<Info> findInfos = infoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(findInfos).hasSize(1);
        assertThat(findInfos.getFirst()).isEqualTo(savedInfo1);

    }

    @Test
    @DisplayName("date 일치하는 info list를 반환한다.")
    void findAllByQuery_date() {

        //Given
        LocalDate date1 = LocalDate.of(2024, 8, 1);
        LocalDate date2 = LocalDate.of(2024, 8, 2);
        Time time = Time.valueOf("12:00:00");

        Info info1 = Info.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date1)
                .time(time)
                .build();

        Info info2 = Info.builder()
                .id(2)
                .movie(movie1)
                .theater(theater1)
                .date(date2)
                .time(time)
                .build();

        Info savedInfo1 = infoRepository.save(info1);
        Info savedInfo2 = infoRepository.save(info2);

        //When
        List<Info> findInfos = infoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date1);

        //Then
        assertThat(findInfos).hasSize(1);
        assertThat(findInfos.getFirst()).isEqualTo(savedInfo1);

    }

    @Test
    @DisplayName("movieName, wideArea, basicArea, date 일치하는 info list를 반환한다.")
    void findAllByQuery_all() {

        //Given
        LocalDate date = LocalDate.of(2024, 8, 1);
        Time time1 = Time.valueOf("12:00:00");
        Time time2 = Time.valueOf("13:30:00");

        Info info1 = Info.builder()
                .id(1)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time1)
                .build();

        Info info2 = Info.builder()
                .id(2)
                .movie(movie1)
                .theater(theater1)
                .date(date)
                .time(time2)
                .build();

        Info savedInfo1 = infoRepository.save(info1);
        Info savedInfo2 = infoRepository.save(info2);

        //When
        List<Info> findInfos = infoRepository.findAllByQuery(movie1.getTitle(), theater1.getWideArea(), theater1.getBasicArea(), date);

        //Then
        assertThat(findInfos).hasSize(2);
        assertThat(findInfos).contains(savedInfo1, savedInfo2);

    }
}