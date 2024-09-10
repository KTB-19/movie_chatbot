package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.dto.MovieInfoDetailsQueryDto;
import com.ktb19.moviechatbot.entity.MovieInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Repository
public interface MovieInfoRepository extends JpaRepository<MovieInfo, Long> {
    @Query("select new com.ktb19.moviechatbot.dto.MovieInfoDetailsQueryDto(i, m, t)" +
            " from MovieInfo i" +
            " left join i.movie m" +
            " left join i.theater t" +
            " where m.title = :movieName" +
            " and t.wideArea = :wideArea" +
            " and t.basicArea = :basicArea" +
            " and i.date = :date")
    List<MovieInfoDetailsQueryDto> findAllByQuery(String movieName, String wideArea, String basicArea, LocalDate date);

    @Query("select new com.ktb19.moviechatbot.dto.MovieInfoDetailsQueryDto(i, m, t)" +
            " from MovieInfo i" +
            " left join i.movie m" +
            " left join i.theater t" +
            " where m.title = :movieName" +
            " and t.wideArea = :wideArea" +
            " and t.basicArea = :basicArea" +
            " and i.date = :date" +
            " and i.time >= :time")
    List<MovieInfoDetailsQueryDto> findAllByQueryAfterTime(
            String movieName,
            String wideArea,
            String basicArea,
            LocalDate date,
            LocalTime time
    );
}
