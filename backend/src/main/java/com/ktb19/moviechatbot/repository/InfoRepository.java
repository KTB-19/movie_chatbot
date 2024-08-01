package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.entity.Info;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.Date;
import java.util.List;

@Repository
public interface InfoRepository extends JpaRepository<Info, Long> {
    @Query("select i from Info i")
    List<Info> findAllByQuery(String movieName, String wideArea, String basicArea, LocalDate date);
}
