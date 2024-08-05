package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.dto.InfoDetailsQueryDto;
import com.ktb19.moviechatbot.entity.Info;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface InfoRepository extends JpaRepository<Info, Long> {
    @Query("select new com.ktb19.moviechatbot.dto.InfoDetailsQueryDto(i, m, t)" +
            " from Info i" +
            " left join i.movie m" +
            " left join i.theater t" +
            " where m.title = :movieName" +
            " and t.wideArea = :wideArea" +
            " and t.basicArea = :basicArea" +
            " and i.date = :date")
    List<InfoDetailsQueryDto> findAllByQuery(String movieName, String wideArea, String basicArea, LocalDate date);
}
