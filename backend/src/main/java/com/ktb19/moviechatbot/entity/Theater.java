package com.ktb19.moviechatbot.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Theater {

    @Id
    @Column(name = "theater_id")
    private Integer id;

    private String name;
    private String wideArea;
    private String basicArea;

    @Builder
    public Theater(Integer id, String name, String wideArea, String basicArea) {
        this.id = id;
        this.name = name;
        this.wideArea = wideArea;
        this.basicArea = basicArea;
    }
}
