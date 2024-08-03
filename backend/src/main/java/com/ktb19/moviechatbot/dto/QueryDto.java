package com.ktb19.moviechatbot.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class QueryDto {

    private String movieName;
    private String region;
    private LocalDate date;
}
