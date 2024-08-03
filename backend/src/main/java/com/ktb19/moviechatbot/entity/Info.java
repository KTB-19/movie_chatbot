package com.ktb19.moviechatbot.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.sql.Time;
import java.time.LocalDate;

@Entity
@Table
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Info {

    @Id
    @Column(name = "info_id")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "movie_id")
    private Movie movie;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "theater_id")
    private Theater theater;

    private LocalDate date;
    private Time time;

    @Builder
    public Info(Integer id, Movie movie, Theater theater, LocalDate date, Time time) {
        this.id = id;
        this.movie = movie;
        this.theater = theater;
        this.date = date;
        this.time = time;
    }
}
