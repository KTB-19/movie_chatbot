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

    private Movie movie;
    private Theater theater;

    @BeforeEach
    void setUp() {
        movie = Movie.builder().id(1).build();
        movie = movieRepository.save(movie);

        theater = Theater.builder().id(1).build();
        theater = theaterRepository.save(theater);
    }

    @Test
    @DisplayName("Info 엔티티 저장 및 조회 테스트")
    void saveAndFindByIdTest() {
        // given
        Info info = Info.builder()
                .id(1)
                .movie(movie)
                .theater(theater)
                .date(LocalDate.now())
                .time(Time.valueOf("12:00:00"))
                .build();

        infoRepository.save(info);

        // when
        Optional<Info> foundInfo = infoRepository.findById(Long.valueOf(info.getId()));

        // then
        assertThat(foundInfo).isPresent();
        assertThat(foundInfo.get().getMovie()).isEqualTo(movie);
        assertThat(foundInfo.get().getTheater()).isEqualTo(theater);
        assertThat(foundInfo.get().getDate()).isEqualTo(info.getDate());
        assertThat(foundInfo.get().getTime()).isEqualTo(info.getTime());
    }

}