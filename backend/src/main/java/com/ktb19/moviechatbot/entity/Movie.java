package com.ktb19.moviechatbot.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Movie {

    @Id
    @Column(name = "movie_id")
    private Integer id;

    private String title;

    @Builder
    public Movie(Integer id, String title) {
        this.id = id;
        this.title = title;
    }
}
